from prisma import Prisma

db = Prisma()
db.connect()
# res = db.user.create(
#     data={
#         "id": "test",
#         "telegramId": "test",
#         "telegramThread": {
#             "create": {
#                 "id": "test",
#                 "platform": "telegram",
#             }
#         },
#     }
# )

res2 = db.transaction.create_many(
    data=[
        {
            "amountOut": "1020",
            "amountIn": "0",
            "category": "Miscellaneous",
            "description": "test transaction",
            "sourceOrPayee": "wallmart",
            "transactionDate": "20230101",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "502",
            "amountIn": "0",
            "category": "Transportation",
            "description": "bus fare",
            "sourceOrPayee": "public transport",
            "transactionDate": "20230201",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "1202",
            "amountIn": "0",
            "category": "Entertainment",
            "description": "movie night",
            "sourceOrPayee": "cinema",
            "transactionDate": "20230205",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "2020",
            "amountIn": "0",
            "category": "RentAndMortgage",
            "description": "monthly rent",
            "sourceOrPayee": "landlord",
            "transactionDate": "20230210",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "302",
            "amountIn": "0",
            "category": "FoodAndDining",
            "description": "takeout dinner",
            "sourceOrPayee": "local restaurant",
            "transactionDate": "20230215",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "802",
            "amountIn": "0",
            "category": "Utilities",
            "description": "electricity bill",
            "sourceOrPayee": "utility company",
            "transactionDate": "20230220",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "235",
            "amountIn": "0",
            "category": "Clothing",
            "description": "new socks",
            "sourceOrPayee": "clothing store",
            "transactionDate": "20230225",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "403",
            "amountIn": "0",
            "category": "Healthcare",
            "description": "prescription medicine",
            "sourceOrPayee": "pharmacy",
            "transactionDate": "20230301",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "1350",
            "amountIn": "0",
            "category": "Education",
            "description": "textbooks",
            "sourceOrPayee": "bookstore",
            "transactionDate": "20230305",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "610",
            "amountIn": "0",
            "category": "Miscellaneous",
            "description": "gift for a friend",
            "sourceOrPayee": "gift shop",
            "transactionDate": "20230310",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "910",
            "amountIn": "0",
            "category": "Grocery",
            "description": "monthly groceries",
            "sourceOrPayee": "supermarket",
            "transactionDate": "20230315",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "710",
            "amountIn": "0",
            "category": "Transportation",
            "description": "gasoline",
            "sourceOrPayee": "gas station",
            "transactionDate": "20230320",
            "currency": "USD",
            "userId": "test",
        },
        {
            "amountOut": "1010",
            "amountIn": "0",
            "category": "Entertainment",
            "description": "concert tickets",
            "sourceOrPayee": "ticket vendor",
            "transactionDate": "20230301",
            "currency": "USD",
            "userId": "test",
        },
    ]
)
# print(res)
print(res2)
db.disconnect()
