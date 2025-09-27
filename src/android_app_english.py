"""
透析供給装置薬液補充アプリ - Android版（英語版）
KivyベースのAndroid対応アプリケーション - 英語UI
"""

import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.theming import ThemeManager
import cv2
import numpy as np
import yaml
from plyer import camera
import threading
import time

from src.medicine_selector import MedicineSelector, MedicineType
from src.camera_manager import CameraManager


class MedicineSelectionScreen(MDScreen):
    """Medicine Selection Screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.medicine_selector = MedicineSelector()
        self.selected_medicine = None
        self.setup_ui()
    
    def setup_ui(self):
        """UI Setup"""
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=20,
            adaptive_height=True
        )
        
        # Title with icon
        title_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=60
        )
        
        title = MDLabel(
            text="💊 Medicine Selection",
            theme_text_color="Primary",
            size_hint_y=None,
            height=50,
            halign="center",
            font_style="H4"
        )
        title_layout.add_widget(title)
        layout.add_widget(title_layout)
        
        # Medicine selection card with elevation
        card = MDCard(
            orientation='vertical',
            padding=15,
            spacing=15,
            size_hint_y=None,
            height=160,
            elevation=4,
            shadow_softness=8,
            shadow_offset=(0, -1)
        )
        
        # Sodium Hypochlorite selection
        sodium_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=8,
            size_hint_y=None,
            height=40
        )
        
        self.sodium_radio = MDCheckbox(
            group='medicine',
            on_release=self.on_medicine_selected
        )
        sodium_label = MDLabel(
            text="🧪 Sodium Hypochlorite",
            theme_text_color="Primary",
            font_style="Body1"
        )
        
        sodium_layout.add_widget(self.sodium_radio)
        sodium_layout.add_widget(sodium_label)
        
        # Acetic Acid selection
        acetic_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=8,
            size_hint_y=None,
            height=40
        )
        
        self.acetic_radio = MDCheckbox(
            group='medicine',
            on_release=self.on_medicine_selected
        )
        acetic_label = MDLabel(
            text="🧪 Acetic Acid",
            theme_text_color="Primary",
            font_style="Body1"
        )
        
        acetic_layout.add_widget(self.acetic_radio)
        acetic_layout.add_widget(acetic_label)
        
        card.add_widget(sodium_layout)
        card.add_widget(acetic_layout)
        layout.add_widget(card)
        
        # Start supply button with icon
        self.start_button = MDRaisedButton(
            text="🚀 Start Supply",
            size_hint_y=None,
            height=50,
            disabled=True,
            on_release=self.start_supply,
            elevation=4,
            font_style="Button"
        )
        layout.add_widget(self.start_button)
        
        self.add_widget(layout)
    
    def on_medicine_selected(self, instance):
        """Medicine selection handler"""
        if instance == self.sodium_radio and instance.active:
            # Clear other selection
            self.acetic_radio.active = False
            self.medicine_selector.select_medicine(MedicineType.SODIUM_HYPOCHLORITE)
            self.selected_medicine = "Sodium Hypochlorite"
        elif instance == self.acetic_radio and instance.active:
            # Clear other selection
            self.sodium_radio.active = False
            self.medicine_selector.select_medicine(MedicineType.ACETIC_ACID)
            self.selected_medicine = "Acetic Acid"
        
        if self.selected_medicine:
            self.start_button.disabled = False
            print(f"Medicine selected: {self.selected_medicine}")
    
    def start_supply(self, instance):
        """Start supply process"""
        if not self.medicine_selector.is_medicine_selected():
            self.show_dialog("Warning", "Please select a medicine")
            return
        
        # Navigate to camera screen
        app = App.get_running_app()
        app.screen_manager.current = 'camera'
        app.camera_screen.start_camera()


class CameraScreen(MDScreen):
    """Camera Screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera_manager = None
        self.is_camera_active = False
        self.setup_ui()
    
    def setup_ui(self):
        """UI Setup"""
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            padding=10
        )
        
        # Camera title
        camera_title = MDLabel(
            text="📷 Camera View",
            theme_text_color="Primary",
            size_hint_y=None,
            height=50,
            halign="center",
            font_style="H4"
        )
        layout.add_widget(camera_title)
        
        # Camera image display with card
        camera_card = MDCard(
            orientation='vertical',
            padding=8,
            size_hint=(1, 0.75),
            elevation=4
        )
        
        self.camera_image = Image(
            allow_stretch=True,
            keep_ratio=True
        )
        camera_card.add_widget(self.camera_image)
        layout.add_widget(camera_card)
        
        # Control buttons
        button_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=8,
            size_hint_y=None,
            height=45
        )
        
        self.camera_button = MDRaisedButton(
            text="📸 Start Camera",
            on_release=self.toggle_camera,
            elevation=4,
            font_style="Button"
        )
        
        self.back_button = MDFlatButton(
            text="⬅️ Back",
            on_release=self.go_back,
            font_style="Button"
        )
        
        button_layout.add_widget(self.camera_button)
        button_layout.add_widget(self.back_button)
        layout.add_widget(button_layout)
        
        self.add_widget(layout)
    
    def start_camera(self):
        """Start camera"""
        if not self.is_camera_active:
            self.toggle_camera()
    
    def toggle_camera(self, instance=None):
        """Toggle camera on/off"""
        if not self.is_camera_active:
            self.activate_camera()
        else:
            self.deactivate_camera()
    
    def activate_camera(self):
        """Activate camera"""
        try:
            # Check if we're on Android or desktop
            import platform
            if platform.system() == "Windows":
                # Desktop camera simulation
                self.simulate_camera()
            else:
                # Android camera activation
                camera.take_picture(
                    filename='temp_camera.jpg',
                    on_complete=self.on_camera_result
                )
            self.is_camera_active = True
            self.camera_button.text = "📸 Stop Camera"
            print("Camera started")
        except Exception as e:
            print(f"Camera activation error: {e}")
            # Fallback to simulation
            self.simulate_camera()
            self.is_camera_active = True
            self.camera_button.text = "📸 Stop Camera"
    
    def simulate_camera(self):
        """Simulate camera for desktop testing"""
        try:
            import cv2
            import numpy as np
            from kivy.clock import Clock
            
            # Try to access webcam
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                # Start continuous capture
                self.capture_event = Clock.schedule_interval(self.capture_frame, 1.0/30.0)  # 30 FPS
                print("Real-time camera started")
            else:
                # Create a test image if no camera available
                self.create_test_image()
        except Exception as e:
            print(f"Camera simulation error: {e}")
            self.create_test_image()
    
    def capture_frame(self, dt):
        """Capture frame continuously"""
        try:
            if hasattr(self, 'cap') and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    # Save the frame
                    cv2.imwrite('temp_camera.jpg', frame)
                    # Use Clock.schedule_once to update UI in main thread
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: self.on_camera_result('temp_camera.jpg'), 0)
        except Exception as e:
            print(f"Frame capture error: {e}")
    
    def create_test_image(self):
        """Create a test image for demonstration"""
        try:
            import cv2
            import numpy as np
            
            # Create a test image with text
            img = np.zeros((480, 640, 3), dtype=np.uint8)
            img.fill(50)  # Dark gray background
            
            # Add text
            cv2.putText(img, "Camera Test", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
            cv2.putText(img, "Medicine Detection", (150, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(img, "Ready for Analysis", (180, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Save test image
            cv2.imwrite('temp_camera.jpg', img)
            self.on_camera_result('temp_camera.jpg')
        except Exception as e:
            print(f"Test image creation error: {e}")
    
    def deactivate_camera(self):
        """Deactivate camera"""
        self.is_camera_active = False
        self.camera_button.text = "📸 Start Camera"
        self.camera_image.texture = None
        
        # Stop continuous capture
        if hasattr(self, 'capture_event'):
            self.capture_event.cancel()
        
        # Release camera
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        
        print("Camera stopped")
    
    def on_camera_result(self, filename):
        """Camera capture result handler"""
        if os.path.exists(filename):
            # Load and display image
            try:
                # Force reload the image
                if hasattr(self, 'camera_image') and self.camera_image:
                    # Clear existing source
                    self.camera_image.source = ''
                    # Set new source
                    self.camera_image.source = filename
                    # Force texture reload
                    self.camera_image.reload()
                    print(f"Camera image updated: {filename}")
            except Exception as e:
                print(f"Image loading error: {e}")
        else:
            print("Failed to capture camera image")
    
    def go_back(self, instance):
        """Go back to previous screen"""
        if self.is_camera_active:
            self.deactivate_camera()
        
        app = App.get_running_app()
        app.screen_manager.current = 'medicine_selection'
    
    def show_dialog(self, title, text):
        """Show dialog"""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()


class DialysisSupplyApp(MDApp):
    """Main Application Class"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None
        self.camera_screen = None
        self.medicine_screen = None
        self.config_data = self.load_config()
    
    def load_config(self):
        """Load configuration file"""
        try:
            with open('config.yaml', 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print("Configuration file not found. Using default settings.")
            return self.get_default_config()
        except Exception as e:
            print(f"Configuration file loading error: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            'camera': {'device_id': 0, 'width': 640, 'height': 480, 'fps': 30},
            'ui': {'window_width': 800, 'window_height': 600, 'title': 'Dialysis Supply App'}
        }
    
    def build(self):
        """Build application"""
        # Theme settings
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        
        # Set mobile-friendly window size
        Window.size = (360, 640)  # Mobile portrait size
        Window.minimum_width = 360
        Window.minimum_height = 640
        
        # Screen manager setup
        self.screen_manager = ScreenManager()
        
        # Medicine selection screen
        self.medicine_screen = MedicineSelectionScreen(name='medicine_selection')
        self.screen_manager.add_widget(self.medicine_screen)
        
        # Camera screen
        self.camera_screen = CameraScreen(name='camera')
        self.screen_manager.add_widget(self.camera_screen)
        
        return self.screen_manager
    
    def on_start(self):
        """Application start handler"""
        print("Dialysis Supply App started")
    
    def on_stop(self):
        """Application stop handler"""
        if self.camera_screen and self.camera_screen.is_camera_active:
            self.camera_screen.deactivate_camera()
        print("Application stopped")


def main():
    """Main function"""
    try:
        app = DialysisSupplyApp()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
