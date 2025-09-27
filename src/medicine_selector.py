"""
薬液選択管理クラス
次亜塩素酸ナトリウムと酢酸の選択を管理
"""

from enum import Enum
from typing import Optional


class MedicineType(Enum):
    """薬液の種類を定義する列挙型"""
    SODIUM_HYPOCHLORITE = "次亜塩素酸ナトリウム"
    ACETIC_ACID = "酢酸"


class MedicineSelector:
    """薬液選択管理クラス"""
    
    def __init__(self):
        """薬液選択管理クラスの初期化"""
        self.selected_medicine: Optional[MedicineType] = None
        self.medicine_types = list(MedicineType)
    
    def select_medicine(self, medicine_type: MedicineType) -> bool:
        """
        薬液を選択
        
        Args:
            medicine_type: 選択する薬液の種類
            
        Returns:
            bool: 選択成功の場合True
        """
        if medicine_type in self.medicine_types:
            self.selected_medicine = medicine_type
            print(f"薬液を選択しました: {medicine_type.value}")
            return True
        else:
            print(f"無効な薬液種類: {medicine_type}")
            return False
    
    def get_selected_medicine(self) -> Optional[MedicineType]:
        """
        選択された薬液を取得
        
        Returns:
            MedicineType: 選択された薬液の種類、未選択の場合はNone
        """
        return self.selected_medicine
    
    def get_selected_medicine_name(self) -> Optional[str]:
        """
        選択された薬液の名前を取得
        
        Returns:
            str: 選択された薬液の名前、未選択の場合はNone
        """
        return self.selected_medicine.value if self.selected_medicine else None
    
    def clear_selection(self):
        """選択をクリア"""
        self.selected_medicine = None
        print("薬液選択をクリアしました")
    
    def is_medicine_selected(self) -> bool:
        """
        薬液が選択されているかチェック
        
        Returns:
            bool: 薬液が選択されている場合True
        """
        return self.selected_medicine is not None
    
    def get_available_medicines(self) -> list[MedicineType]:
        """
        利用可能な薬液のリストを取得
        
        Returns:
            list[MedicineType]: 利用可能な薬液のリスト
        """
        return self.medicine_types.copy()
    
    def get_medicine_by_name(self, name: str) -> Optional[MedicineType]:
        """
        名前で薬液の種類を取得
        
        Args:
            name: 薬液の名前
            
        Returns:
            MedicineType: 該当する薬液の種類、見つからない場合はNone
        """
        for medicine in self.medicine_types:
            if medicine.value == name:
                return medicine
        return None
