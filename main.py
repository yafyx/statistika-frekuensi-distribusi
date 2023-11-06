import math

import numpy as np
import pandas as pd
from tabulate import tabulate

data = [
    60, 64, 83, 92, 94, 80, 81, 59, 67, 80,
    90, 73, 93, 71, 76, 79, 80, 78, 65, 82,
    75, 84, 79, 84, 64, 81, 85, 90, 69, 59,
    72, 87, 76, 87, 78, 72, 53, 60, 89, 87,
    58, 92, 73, 91, 60, 65, 73, 67, 75, 64,
]

# data = [
#     176, 153, 158, 144, 169, 144, 152, 148,
#     168, 166, 154, 160, 168, 174, 168, 149,
#     166, 170, 170, 171, 161, 174, 161, 167,
#     171, 173, 155, 168, 144, 171, 152, 173,
#     147, 168, 148, 173, 144, 146, 155, 168,
#     141, 176, 156, 156, 167, 176, 152, 174,
#     162, 155, 143, 139, 154, 143, 167, 151,
#     155, 175, 154, 153, 162, 156, 174, 154,
#     143, 162, 146, 168, 172, 162, 157, 147,
#     173, 168, 161, 172, 159, 171, 152, 156
# ]

n = len(data)
r = max(data) - min(data)
k_ceil = math.ceil(1 + 3.322 * math.log10(n))
k_floor = math.floor(1 + 3.322 * math.log10(n))
i = math.ceil(r / k_ceil)

print("n = ", n)
print("r = ", max(data), "-", min(data), "=", r, " ")
print("k ceiling = 1 + 3.322 log 10(", n, ") = ", k_ceil)
print("k floor = 1 + 3.322 log 10(", n, ") = ", k_floor)
print("i = r/k = ", r, "/", k_ceil, "=", i, "\n")

print("TDF: ")
df = pd.DataFrame(
    columns=[
        "Kelas",
        "Titik Tengah",
        "Frekuensi",
        "Frekuensi Relatif",
        "Frekuensi Relatif (%)",
    ]
)

for j in range(k_ceil):
    batas_bawah = min(data) + i * j
    batas_atas = batas_bawah + i - 1
    titik_tengah = (batas_bawah + batas_atas) / 2
    frekuensi = len([x for x in data if batas_bawah <= x <= batas_atas])
    frekuensi_relatif = frekuensi / n
    frekuensi_relatif_persen = frekuensi_relatif * 100

    df.loc[j] = [
        f"{batas_bawah}-{batas_atas}",
        titik_tengah,
        frekuensi,
        frekuensi_relatif,
        frekuensi_relatif_persen,
    ]

df["fixi"] = df["Frekuensi"] * df["Titik Tengah"]

M = df.loc[k_ceil // 2, "Titik Tengah"]

df["M"] = M
df["di"] = df["Titik Tengah"] - M
df["fidi"] = df["Frekuensi"] * df["di"]

df["Fk"] = np.cumsum(df["Frekuensi"])

df.loc[k_ceil] = [
    "Σ",
    "",
    df["Frekuensi"].sum(),
    "",
    df["Frekuensi Relatif (%)"].sum(),
    df["fixi"].sum(),
    "",
    "",
    df["fidi"].sum(),
    "",
]

print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
print()

print("Mean:")
mean_fixi = df.loc[k_ceil, "fixi"] / n
mean_fidi = M + df.loc[k_ceil, "fidi"] / n

print(f"x̄ = {df.loc[k_ceil, 'fixi']}/{n} = {mean_fixi}")
print(f"x̄ = {M} + ({df.loc[k_ceil, 'fidi']}/{n}) = {mean_fidi} \n")

print("Modus:")
max_freq = df.iloc[:-1]["Frekuensi"].max()
modus_kelas = df[df["Frekuensi"] == max_freq].iloc[0]["Kelas"]
modus_batas_bawah = int(modus_kelas.split("-")[0])
modus_index = df[df["Kelas"] == modus_kelas].index[0]
prev_freq = df.loc[modus_index - 1, "Frekuensi"]
next_freq = df.loc[modus_index + 1, "Frekuensi"]
d1 = max_freq - prev_freq
d2 = max_freq - next_freq
modus = modus_batas_bawah + i * (d1 / (d1 + d2))
print(f"Modus = {modus_batas_bawah} + {i}({d1}/{d1}+{d2})")
print(f"      = {modus_batas_bawah} + {i}*{d1/(d1+d2):.5f}...")
print(
    f"      = {modus_batas_bawah + i*(d1/(d1+d2)):.5f} ≈ {round(modus_batas_bawah + i*(d1/(d1+d2)))}"
)
print()

print("Median:")
median_loc = n / 2
median_kelas = ""
cumulative_freq = 0 
for index, row in df.iterrows():
    cumulative_freq += row["Frekuensi"]
    if cumulative_freq >= median_loc:
        median_kelas = row["Kelas"]
        break
median_batas_bawah = int(median_kelas.split("-")[0])
median_frekuensi_kelas = df[df["Kelas"] == median_kelas]["Frekuensi"].iloc[0]
prev_cumulative_freq = cumulative_freq - median_frekuensi_kelas
s = median_loc - prev_cumulative_freq
interval = i
TBB = median_batas_bawah - 0.5
TBA = median_batas_bawah + interval - 0.5
fm = median_frekuensi_kelas
s_ = cumulative_freq - median_loc
median = TBB + interval * (s / fm)

print(tabulate([
    [f"Letak Median = n/2 = {n}/2 = {median_loc} → terletak di kelas {median_kelas}"],
    [f"Kelas Median = {median_kelas}"],
    [f"TBB Kelas Median = {TBB} | TBA Kelas Median = {TBA}"],
    [f"Frekuensi Kelas Median (fM) = {fm}"],
    [f"Frek. Kumulatif sebelum Kelas Median = {prev_cumulative_freq} → s = {cumulative_freq} - {prev_cumulative_freq} = {s}"],
    [f"Frek. Kumulatif sampai Kelas Median = {cumulative_freq} → s’ = {cumulative_freq} - {median_loc} = {s_}"],
    [f"TBB Kelas Median + i(s/fm)\n"
    f"= {TBB} + {interval}({s}/{fm:.1f})\n"
    f"= {TBB} + {interval * (s / fm):.1f} = {median:.3f} ≈ {round(median, 1)}"],
    [f"TBA Kelas Median - i(s'/fm)\n"
    f"= {TBA} - {interval}({s_}/{fm:.1f})\n"
    f"= {TBA} - {interval * (s_ / fm):.1f} = {median:.3f} ≈ {round(median, 1)}"]
], tablefmt='rounded_grid'))
print()

print("Kuartil ke - q:")
q = 3
letak_kuartil = q * n / 4
cumulative_freq = 0
kelas_kuartil = ""
for index, row in df.iterrows():
    cumulative_freq += row["Frekuensi"]
    if cumulative_freq >= letak_kuartil:
        kelas_kuartil = row["Kelas"]
        break
batas_bawah_kuartil = int(kelas_kuartil.split("-")[0])
frekuensi_kelas_kuartil = df[df["Kelas"] == kelas_kuartil]["Frekuensi"].iloc[0]
prev_cumulative_freq = cumulative_freq - frekuensi_kelas_kuartil
s = letak_kuartil - prev_cumulative_freq
interval = i
TBB = batas_bawah_kuartil - 0.5
TBA = batas_bawah_kuartil + interval - 0.5
fq = frekuensi_kelas_kuartil
s_ = cumulative_freq - letak_kuartil
kuartil = TBB + interval * (s / fq)

print(tabulate([
    [f"Letak Kuartil ke {q} = {q} x {n}/4 = {letak_kuartil}"],
    [f"Kelas Kuartil ke {q} = {kelas_kuartil}"],
    [f"TBB Kelas Kuartil ke {q} = {TBB} | TBA Kelas Kuartil ke {q} = {TBA}"],
    [f"Frekuensi Kelas Kuartil ke {q} (fQ) = {fq}"],
    [f"Frek. Kumulatif sebelum Kelas Kuartil ke {q} = {prev_cumulative_freq} → s = {letak_kuartil} - {prev_cumulative_freq} = {s}"],
    [f"Frek. Kumulatif sampai Kelas Kuartil ke {q} = {cumulative_freq} → s’ = {cumulative_freq} - {letak_kuartil} = {s_}"],
    [f"TBB Kelas Kuartil ke {q} + i(s/fq)\n"
    f"= {TBB} + {interval}({s}/{fq:.1f})\n"
    f"= {TBB} + {interval * (s / fq):.1f} = {kuartil:.2f}"],
    [f"TBA Kelas Kuartil ke {q} - i(s'/fq)\n"
    f"= {TBA} - {interval}({s_}/{fq:.1f})\n"
    f"= {TBA} - {interval * (s_ / fq):.1f} = {kuartil:.2f}"]
], tablefmt='rounded_grid'))
print()

print("Desil ke - d:")
d = 7
letak_desil = d * n / 10
cumulative_freq = 0
kelas_desil = ""
for index, row in df.iterrows():
    cumulative_freq += row["Frekuensi"]
    if cumulative_freq >= letak_desil:
        kelas_desil = row["Kelas"]
        break
batas_bawah_desil = int(kelas_desil.split("-")[0])
frekuensi_kelas_desil = df[df["Kelas"] == kelas_desil]["Frekuensi"].iloc[0]
prev_cumulative_freq = cumulative_freq - frekuensi_kelas_desil
s = letak_desil - prev_cumulative_freq
interval = i
TBB = batas_bawah_desil - 0.5
TBA = batas_bawah_desil + interval - 0.5
fd = frekuensi_kelas_desil
s_ = cumulative_freq - letak_desil
desil = TBB + interval * (s / fd)
desil = TBA - interval * (s_ / fd)

print(tabulate([
    [f"Letak Desil ke {d} = {d} x {n}/10 = {letak_desil}"],
    [f"Kelas Desil ke {d} = {kelas_desil}"],
    [f"TBB Kelas Desil ke {d} = {TBB} | TBA Kelas Desil ke {d} = {TBA}"],
    [f"Frekuensi Kelas Desil ke {d} (fD) = {fd}"],
    [f"Frek. Kumulatif sebelum Kelas Desil ke {d} = {prev_cumulative_freq} → s = {letak_desil} - {prev_cumulative_freq} = {s}"],
    [f"Frek. Kumulatif sampai Kelas Desil ke {d} = {cumulative_freq} → s’ = {cumulative_freq} - {letak_desil} = {s_}"],
    [f"TBB Kelas Desil ke {d} + i(s/fd)\n"
    f"= {TBB} + {interval}({s}/{fd:.1f})\n"
    f"= {TBB} + {interval * (s / fd):.1f} = {desil:.2f}"],
    [f"TBA Kelas Desil ke {d} - i(s'/fd)\n"
    f"= {TBA} - {interval}({s_}/{fd:.1f})\n"
    f"= {TBA} - {interval * (s_ / fd):.1f} = {desil:.2f}"]
], tablefmt='rounded_grid'))
print()

print("Persentil ke - p:")
p = 89
letak_persentil = p * n / 100
cumulative_freq = 0
kelas_persentil = ""
for index, row in df.iterrows():
    cumulative_freq += row["Frekuensi"]
    if cumulative_freq >= letak_persentil:
        kelas_persentil = row["Kelas"]
        break
batas_bawah_persentil = int(kelas_persentil.split("-")[0])
frekuensi_kelas_persentil = df[df["Kelas"] == kelas_persentil]["Frekuensi"].iloc[0]
prev_cumulative_freq = cumulative_freq - frekuensi_kelas_persentil
s = letak_persentil - prev_cumulative_freq
interval = i
TBB = batas_bawah_persentil - 0.5
TBA = batas_bawah_persentil + interval - 0.5
fp = frekuensi_kelas_persentil
s_ = cumulative_freq - letak_persentil
persentil = TBB + interval * (s / fp)
persentil = TBA - interval * (s_ / fp)

print(tabulate([
    [f"Letak Persentil ke {p} = {p} x {n}/100 = {letak_persentil}"],
    [f"Kelas Persentil ke {p} = {kelas_persentil}"],
    [f"TBB Kelas Persentil ke {p} = {TBB} | TBA Kelas Persentil ke {p} = {TBA}"],
    [f"Frekuensi Kelas Persentil ke {p} (fP) = {fp}"],
    [f"Frek. Kumulatif sebelum Kelas Persentil ke {p} = {prev_cumulative_freq} → s = {letak_persentil} - {prev_cumulative_freq} = {s}"],
    [f"Frek. Kumulatif sampai Kelas Persentil ke {p} = {cumulative_freq} → s’ = {cumulative_freq} - {letak_persentil} = {s_}"],
    [f"TBB Kelas Persentil ke {p} + i(s/fp)\n"
    f"= {TBB} + {interval}({s}/{fp:.1f})\n"
    f"= {TBB} + {interval * (s / fp):.1f} = {persentil:.2f}"],
    [f"TBA Kelas Persentil ke {p} - i(s'/fp)\n"
    f"= {TBA} - {interval}({s_}/{fp:.1f})\n"
    f"= {TBA} - {interval * (s_ / fp):.1f} = {persentil:.2f}"]
], tablefmt='rounded_grid'))
print()
