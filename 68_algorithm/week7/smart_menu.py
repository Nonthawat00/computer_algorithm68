from typing import List, Dict, Optional


def main():
    items: List[Dict] = []

    while True:
            print("\n=== Smart Menu Analyzer ===")
            print("1) เพิ่มเมนู")
            print("2) ลบเมนู")
            print("3) แสดงรายการทั้งหมด")
            print("4) หาถูกสุด/แพงสุด")
            print("5) ยอดรวม/ค่าเฉลี่ย")
            print("6) นับเมนูที่ราคา > X")
            print("7) เรียงราคา (Bubble/Selection)")
            print("0) ออก")

            choice = input("เลือกเมนู : ").strip()

            if choice == "1":
                add_item(items)
            
            elif choice == "2":
                remove_item(items)
            elif choice == "3":
                show_items(items)
            elif choice == "4":
                find_min_max(items)
            elif choice == "5":
                total_and_average(items)   #ค่าเฉลี่ย ราคา
            elif choice == "6":
                count_greater_than(items)   #จำนวนรายการสินค้า 
            elif choice == "7":
                sort_menu(items) #เรียงลำดับ (ชื่อรายการสินค้า A-Z, Z-A ราคา  น้อยไปมาก มากไปน้อย) 

          
            elif choice == "0":
                print("👋 ออกจากโปรแกรม")
                break
            else:
                print("❌ กรุณาเลือกเมนูให้ถูกต้อง")


def add_item(items: List[Dict]) -> None:
    name = input("ชื่อเมนู: ").strip()
    if not name:
        print("❌ ชื่อเมนูห้ามว่าง")
        return
    price = input_float("ราคา: ")
    items.append({"name": name, "price": price})
    print("✅ เพิ่มเมนูเรียบร้อย")


def remove_item(items: List[Dict]) -> None:
    if not items:
        print("❌ ยังไม่มีเมนู")
        return
    show_items(items)
    idx = input_int("ใส่ลำดับเมนูที่จะลบ: ")
    if idx < 1 or idx > len(items):
        print("❌ ลำดับไม่ถูกต้อง")
        return
    removed = items.pop(idx - 1)
    print(f"✅ ลบเมนู: {removed['name']} ราคา {removed['price']:.2f} บาท")

def show_items(items: List[Dict]) -> None:
    if not items:
        print("❌ ยังไม่มีเมนู")
        return
    print("\n--- รายการเมนู ---")
    for i, it in enumerate(items, start=1):
        print(f"{i:>2}) {it['name']:<20} {it['price']:>8.2f} บาท")
    print("------------------\n")


def input_int(prompt: str) -> int:
    """รับ int แบบปลอดภัย"""
    while True:
        s = input(prompt).strip()
        try:
            v = int(s)
            return v
        except ValueError:
            print("❌ กรุณากรอกเป็นจำนวนเต็ม")

def input_float(prompt: str) -> float:
    """รับ float แบบปลอดภัย"""
    while True:
        s = input(prompt).strip()
        try:
            v = float(s)
            if v < 0:
                print("❌ ราคา/จำนวนต้องไม่ติดลบ")
                continue
            return v
        except ValueError:
            print("❌ กรุณากรอกเป็นตัวเลข")

def find_min_max(items: List[Dict]) -> None:
    if not items:
        print("❌ ยังไม่มีเมนู")
        return
    min_item = min(items, key=lambda x: x["price"])
    max_item = max(items, key=lambda x: x["price"])
    print(f"💸 ถูกสุด: {min_item['name']} = {min_item['price']:.2f} บาท")
    print(f"💰 แพงสุด: {max_item['name']} = {max_item['price']:.2f} บาท")

def total_and_average(items: List[Dict]) -> None:
    if not items:
        print("❌ ยังไม่มีเมนู")
        return
    
    total = sum(item['price'] for item in items)
    avg = total / len(items)
    
    print(f"\n💵 ราคารวมทั้งหมด: {total:.2f} บาท")
    print(f"📊 ราคาเฉลี่ย:     {avg:.2f} บาท")

def count_greater_than(items: List[Dict]) -> None:
    if not items:
        print("❌ ยังไม่มีเมนู")
        return
        
    target = input_float("นับเมนูที่ราคามากกว่าเท่าไหร่? : ")
    count = 0
    print(f"\n--- รายการที่ราคา > {target} ---")
    for item in items:
        if item['price'] > target:
            print(f"- {item['name']} ({item['price']:.2f})")
            count += 1
            
    if count == 0:
        print("ไม่มีรายการที่ราคามากกว่าที่กำหนด")
    else:
        print(f"📌 รวมทั้งหมด: {count} รายการ")

def count_items_greater_than(items: List[Dict]) -> None:
    if not items:
        print("❌ ยังไม่มีเมนู")
        return
        
    target = input_float("นับเมนูที่ราคามากกว่าเท่าไหร่? : ")
    count = 0
    print(f"\n--- รายการที่ราคา > {target} ---")
    for item in items:
        if item['price'] > target:
            print(f"- {item['name']} ({item['price']:.2f})")
            count += 1
            
    if count == 0:
        print("ไม่มีรายการที่ราคามากกว่าที่กำหนด")
    else:
        print(f"📌 รวมทั้งหมด: {count} รายการ")


def sort_menu(items: List[Dict]) -> None:
    if not items:
        print("❌ ยังไม่มีเมนู")
        return

    print("\nเลือกรูปแบบการเรียงลำดับชื่อ:")
    print("1) เรียง A -> Z (ก -> ฮ)")
    print("2) เรียง Z -> A (ฮ -> ก)")
    
    sub_choice = input("เลือก: ").strip()
    
    if sub_choice not in ("1", "2"):
        print("❌ ตัวเลือกไม่ถูกต้อง กลับสู่เมนูหลัก")
        return

    
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            should_swap = False
            
            
            name_current = items[j]['name']
            name_next = items[j + 1]['name']
            
            if sub_choice == "1": 
                
                if name_current > name_next:
                    should_swap = True
            else:
                
                if name_current < name_next:
                    should_swap = True
            
            if should_swap:
                
                items[j], items[j + 1] = items[j + 1], items[j]
    
    mode_text = "A -> Z" if sub_choice == "1" else "Z -> A"
    print(f"✅ เรียงลำดับชื่อ ({mode_text}) เรียบร้อย")
    show_items(items)



def test():
    print("Test")   

if __name__ == "__main__":
    main()
