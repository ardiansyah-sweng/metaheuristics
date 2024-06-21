import seaborn as sns
import matplotlib.pyplot as plt

# Contoh data
# Menggunakan dataset bawaan seaborn sebagai contoh
data = sns.load_dataset("tips")

# Membuat boxplot
sns.boxplot(x="day", y="total_bill", data=data)

# Menampilkan boxplot
plt.show()
