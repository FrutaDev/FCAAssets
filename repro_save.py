import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FCAAssets.settings')
django.setup()

from storage.models import Storage, Labs, Types, Brand

def test_storage_save():
    print("Testing Storage.save() logic...")
    
    # Create dummies if needed
    try:
        lab = Labs.objects.first()
        if not lab:
            lab = Labs.objects.create(lab_name="Test Lab")
            
        type_obj = Types.objects.first()
        if not type_obj:
            type_obj = Types.objects.create(type_name="Test Type")
            
        # 1. Test logic with date far in future
        s = Storage(
            name=type_obj,
            lab_name=lab,
            acquisition_date=date.today(),
            upcoming_maintenance=date.today() + timedelta(days=60) # > 30 days
        )
        s.save()
        print(f"Case 1 (>30 days): Status is '{s.necessary_maintenance}'. Expected 'AD'.")
        
        # 2. Test logic with date soon (por vencer)
        s2 = Storage(
            name=type_obj,
            lab_name=lab,
            acquisition_date=date.today(),
            upcoming_maintenance=date.today() + timedelta(days=10) # > 0 and <= 30
        )
        s2.save()
        print(f"Case 2 (10 days): Status is '{s2.necessary_maintenance}'. Expected 'PV'.")

        # 3. Test logic with date passed (vencido)
        s3 = Storage(
            name=type_obj,
            lab_name=lab,
            acquisition_date=date.today(),
            upcoming_maintenance=date.today() - timedelta(days=1) # < 0
        )
        s3.save()
        print(f"Case 3 (-1 days): Status is '{s3.necessary_maintenance}'. Expected 'VE'.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_storage_save()
