from src.administration.admins.models import (
    StockIn, StockOut, StockOutJudicial, Transaction, Transfer,
    StockInJudicial, TransferJudicial, TransactionJudicial,
)
from src.accounts.models import (
    City, User, Treasury
)

from faker import Faker

fake = Faker()

""" HELPERS FUNCTIONS """


def model_fake_init(model_name):
    print("")
    print(f"__ START FAKE DATA __ ({model_name})")


def model_fake_end(model_name):
    print(f"__ END FAKE DATA __ ({model_name})")
    print("")


def fake_cities(limit=10):
    model_fake_init("City")

    count = 1
    for i in range(limit):
        obj = City.objects.create(name=fake.city())
        print(f"{count} - {obj} - record added to database")
        count += 1

    model_fake_end("City")


def fake_treasuries():
    model_fake_init("Treasury")

    count = 1
    for city in City.objects.all():
        # obj = Treasury.objects.create(name=city.name, city=city)
        obj = Treasury.objects.create(
            name=city.name, city=city,
            j30=100, j35=100, j50=100, j100=100, j500=100, j1000=100, j2000=100, j3000=100, j5000=100, j10000=100,
            j15000=100,
            s100=100, s150=100, s200=100, s250=100, s300=100, s400=100, s500=100, s750=100, s1000=100, s2000=100,
            s3000=100, s5000=100, s10000=100, s25000=100, s50000=100,
        )
        print(f"{count} - {obj} - record added to database")
        count += 1

    model_fake_end("Treasury")


def fake_users():
    users = {
        "admin": {
            "first_name": "admin",
            "last_name": "admin",
            "username": "admin",
            "email": "admin@exarth.com",
            "password": "poiuyt0987654",
            "is_active": True,
        },
        "staff": {
            "first_name": "staff",
            "last_name": "staff",
            "username": "staff",
            "email": "staff@exarth.com",
            "password": "poiuyt0987654",
            "is_active": True,
        },
        "staff2": {
            "first_name": "staff2",
            "last_name": "staff2",
            "username": "staff2",
            "email": "staff2@exarth.com",
            "password": "poiuyt0987654",
            "is_active": True,
        },
    }

    model_fake_init("User")

    # create users from the above dict records
    User.objects.bulk_create([
        User(**users["admin"]),
        User(**users["staff"]),
        User(**users["staff2"]),
    ])
    for user in User.objects.all():
        print(f"{user} - record added to database")

    model_fake_end("User")


def fake_stock_in(limit=10):
    model_fake_init("StockIn")

    count = 1
    for i in range(limit):
        obj = StockIn.objects.create(
            source_treasury=Treasury.objects.first(),
            s100=1, s150=0, s200=0, s250=0, s300=0, s400=0, s500=0, s750=0, s1000=0, s2000=0,
            s3000=0, s5000=0, s10000=0, s25000=0, s50000=0,
            user=User.objects.first()
        )
        print(f"{count} - {obj} - record added to database")
        count += 1

    model_fake_end("StockIn")


def fake_stock_out(limit=10):
    model_fake_init("StockOut")

    count = 1
    for i in range(limit):
        obj = StockOut.objects.create(
            source_treasury=Treasury.objects.first(),
            s100=1, s150=0, s200=0, s250=0, s300=0, s400=0, s500=0, s750=0, s1000=0, s2000=0,
            s3000=0, s5000=0, s10000=0, s25000=0, s50000=0,
            user=User.objects.first()
        )
        print(f"{count} - {obj} - record added to database")
        count += 1

    model_fake_end("StockOut")


def fake_stock_in_judicial(limit=10):
    model_fake_init("StockInJudicial")

    count = 1
    for i in range(limit):
        obj = StockInJudicial.objects.create(
            source_treasury=Treasury.objects.first(),
            j30=1, j35=0, j50=0, j100=0, j500=0, j1000=0, j2000=0, j3000=0, j5000=0, j10000=0,
            j15000=0,
            user=User.objects.first()
        )
        print(f"{count} - {obj} - record added to database")
        count += 1

    model_fake_end("StockInJudicial")


def fake_stock_out_judicial(limit: int = 10):
    model_fake_init("StockOutJudicial")

    count: int = 1
    for i in range(limit):
        obj = StockOutJudicial.objects.create(
            source_treasury=Treasury.objects.first(),
            j30=1, j35=0, j50=0, j100=0, j500=0, j1000=0, j2000=0, j3000=0, j5000=0, j10000=0,
            j15000=0,
            user=User.objects.first()
        )
        print(f"{count} - {obj} - record added to database")
        count += 1

    model_fake_end("StockOutJudicial")


def main():
    fake_cities()
    fake_treasuries()
    fake_users()
    fake_stock_in()
    fake_stock_out()
    fake_stock_in_judicial()
    fake_stock_out_judicial()


if __name__ == "__main__":
    main()
