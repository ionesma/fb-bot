from datetime import datetime

msg = input("კლიენტი: ").lower().strip()

keywords = [
    "სარბენი",
    "ბილიკი",
    "ბილკი",
    "sarbeni",
    "sarbeni",
    "biliki",
    "bilik",
    "treadmill",
    "дорожка",
    "беговая",
    "ფასი",
    "fasi",
    "price",
    "რამდენი",
    "ramdeni",
]

difference_words = [
    "განსხვავება",
    "რა განსხვავებაა",
    "difference",
    "raznica",
    "разница"
]

if any(word in msg for word in keywords):

    print("""
გამარჯობა 👋

გვაქვს 2 მოდელი:

✅ სტანდარტული მოდელი - 280 ლარი

✅ პრემიუმ მოდელი - 380 ლარი
(უფრო ძლიერი და გამძლე ძრავით)

🚚 მიწოდება - 30 ლარი

თუ გაინტერესებთ განსხვავება, დაწერეთ:
"განსხვავება"
""")

    answer = input("\nპასუხი: ").lower()

    if any(word in answer for word in difference_words):

        print("""
📌 განსხვავება:

280 ლარიანი მოდელი
✔ ყოველდღიური გამოყენებისთვის

380 ლარიანი მოდელი
✔ უფრო ძლიერი ძრავით
✔ უფრო გამძლე დატვირთვებისთვის
✔ რეკომენდებულია ხშირი გამოყენებისთვის
""")

        answer = input("\nრომელ მოდელს ირჩევთ? ")

    print("\nშეკვეთის გასაფორმებლად შეავსეთ:")

    name = input("სახელი და გვარი: ")
    phone = input("ტელეფონი: ")
    address = input("მისამართი: ")

    order_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(
            f"{order_date} | "
            f"{answer} | "
            f"{name} | "
            f"{phone} | "
            f"{address}\n"
        )

    print("""
✅ შეკვეთა მიღებულია

მონაცემები წარმატებით შეინახა.
მალე დაგიკავშირდებით.
""")

else:

    print("""
სამწუხაროდ ვერ გავიგე მოთხოვნა.

შეგიძლიათ დაწეროთ:

• სარბენი ბილიკი
• sarbeni biliki
• treadmill
• беговая дорожка
• ფასი
• რამდენი ღირს
""")