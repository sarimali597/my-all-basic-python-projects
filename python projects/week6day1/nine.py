days = ["day1", "day2", "day3", "day4"]
sales1 = [2000, 500, 5000, 7200]
sales2 = [26000, 200, 13000, 5200]
plt.bar(days, sales1,label="Shop-01")
plt.bar(days, sales2,label="Shop-02")
plt.xlabel("Days")
plt.ylabel("Sales")
plt.title("Income of shop")
plt.legend()
plt.show()