import logging
import math

import numpy as np
import pandas as pd
from tabulate import tabulate

logging.basicConfig(level=logging.INFO)


def read_data(file_name):
    try:
        with open(file_name, "r") as f:
            data = [int(x) for x in f.read().split(",")]
        return data
    except Exception as e:
        logging.error(f"Terjadi kesalahan saat membaca file: {e}")
        return []


def print_data(data):
    logging.info("Data:")
    for i in range(0, len(data), 10):
        logging.info(*data[i : i + 10])
    logging.info("")


def get_k(data, k_type):
    if k_type == "c":
        k = math.ceil(1 + 3.322 * math.log10(len(data)))
    elif k_type == "f":
        k = math.floor(1 + 3.322 * math.log10(len(data)))
    else:
        logging.warning(
            "Jenis pembulatan tidak valid. Menggunakan ceiling sebagai default."
        )
        k = math.ceil(1 + 3.322 * math.log10(len(data)))
    return k, k_type


def get_user_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            logging.error("Input tidak valid. Silakan masukkan bilangan Bulat.")


def main():
    data = read_data("data.txt")
    print_data(data)
    k_type = ""
    while k_type not in ["c", "f"]:
        k_type = input("Pilih tipe pembulatan k (ceiling(c)/floor(f)): ")
    k, k_type = get_k(data, k_type)
    q = int(input("Letak kuartil keberapa yang ingin dicari? "))
    d = int(input("Letak desil keberapa yang ingin dicari? "))
    p = int(input("Letak persentil keberapa yang ingin dicari? \n"))
    n = len(data)
    r = max(data) - min(data)
    i = math.ceil(r / k)
    print(f"n = {n}")
    print(f"r = {max(data)} - {min(data)} = {r}")
    print(f"k {k_type} = 1 + 3.322 log 10({n}) = {k}")
    print(f"i = r/k = {r} / {k} = {i}\n")
    print("TDF: ")

    df = pd.DataFrame(
        columns=[
            "Kelas",
            "Titik Tengah",
            "Frekuensi",
            "Frekuensi Relatif",
            "Frekuensi Relatif (%)",
            "fixi",
            "M",
            "di",
            "fidi",
            "Fk",
        ]
    )

    total_frekuensi = 0
    total_fixi = 0
    total_fidi = 0

    for j in range(k):
        batas_bawah = min(data) + i * j
        batas_atas = batas_bawah + i - 1
        titik_tengah = (batas_bawah + batas_atas) / 2
        frekuensi = len([x for x in data if batas_bawah <= x <= batas_atas])
        frekuensi_relatif = frekuensi / n
        frekuensi_relatif_persen = frekuensi_relatif * 100
        fixi = frekuensi * titik_tengah
        M = (min(data) + max(data)) / 2
        di = titik_tengah - M
        fidi = frekuensi * di
        total_frekuensi += frekuensi
        total_fixi += fixi
        total_fidi += fidi
        Fk = total_frekuensi

        df.loc[j] = [
            f"{batas_bawah}-{batas_atas}",
            titik_tengah,
            frekuensi,
            frekuensi_relatif,
            frekuensi_relatif_persen,
            fixi,
            M,
            di,
            fidi,
            Fk,
        ]

    df.loc[k] = [
        "Σ",
        "",
        total_frekuensi,
        "",
        total_frekuensi / n * 100,
        total_fixi,
        "",
        "",
        total_fidi,
        "",
    ]

    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    print()

    print("Mean:")
    mean_fixi = df.loc[k, "fixi"] / n
    mean_fidi = M + df.loc[k, "fidi"] / n

    print(f"x̄ = {df.loc[k, 'fixi']}/{n} = {mean_fixi}")
    print(f"x̄ = {M} + ({df.loc[k, 'fidi']}/{n}) = {mean_fidi} \n")

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

    print(
        tabulate(
            [
                [
                    f"Letak Median = n/2 = {n}/2 = {median_loc} → terletak di kelas {median_kelas}"
                ],
                [f"Kelas Median = {median_kelas}"],
                [f"TBB Kelas Median = {TBB} | TBA Kelas Median = {TBA}"],
                [f"Frekuensi Kelas Median (fM) = {fm}"],
                [
                    f"Frek. Kumulatif sebelum Kelas Median = {prev_cumulative_freq} → s = {cumulative_freq} - {prev_cumulative_freq} = {s}"
                ],
                [
                    f"Frek. Kumulatif sampai Kelas Median = {cumulative_freq} → s’ = {cumulative_freq} - {median_loc} = {s_}"
                ],
                [
                    f"TBB Kelas Median + i(s/fm)\n"
                    f"= {TBB} + {interval}({s}/{fm:.1f})\n"
                    f"= {TBB} + {interval * (s / fm):.1f} = {median:.3f} ≈ {round(median, 1)}"
                ],
                [
                    f"TBA Kelas Median - i(s'/fm)\n"
                    f"= {TBA} - {interval}({s_}/{fm:.1f})\n"
                    f"= {TBA} - {interval * (s_ / fm):.1f} = {median:.3f} ≈ {round(median, 1)}"
                ],
            ],
            tablefmt="rounded_grid",
        )
    )
    print()

    print("Kuartil ke - q:")
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

    print(
        tabulate(
            [
                [f"Letak Kuartil ke {q} = {q} x {n}/4 = {letak_kuartil}"],
                [f"Kelas Kuartil ke {q} = {kelas_kuartil}"],
                [
                    f"TBB Kelas Kuartil ke {q} = {TBB} | TBA Kelas Kuartil ke {q} = {TBA}"
                ],
                [f"Frekuensi Kelas Kuartil ke {q} (fQ) = {fq}"],
                [
                    f"Frek. Kumulatif sebelum Kelas Kuartil ke {q} = {prev_cumulative_freq} → s = {letak_kuartil} - {prev_cumulative_freq} = {s}"
                ],
                [
                    f"Frek. Kumulatif sampai Kelas Kuartil ke {q} = {cumulative_freq} → s’ = {cumulative_freq} - {letak_kuartil} = {s_}"
                ],
                [
                    f"TBB Kelas Kuartil ke {q} + i(s/fq)\n"
                    f"= {TBB} + {interval}({s}/{fq:.1f})\n"
                    f"= {TBB} + {interval * (s / fq):.1f} = {kuartil:.2f}"
                ],
                [
                    f"TBA Kelas Kuartil ke {q} - i(s'/fq)\n"
                    f"= {TBA} - {interval}({s_}/{fq:.1f})\n"
                    f"= {TBA} - {interval * (s_ / fq):.1f} = {kuartil:.2f}"
                ],
            ],
            tablefmt="rounded_grid",
        )
    )
    print()

    print("Desil ke - d:")
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

    print(
        tabulate(
            [
                [f"Letak Desil ke {d} = {d} x {n}/10 = {letak_desil}"],
                [f"Kelas Desil ke {d} = {kelas_desil}"],
                [f"TBB Kelas Desil ke {d} = {TBB} | TBA Kelas Desil ke {d} = {TBA}"],
                [f"Frekuensi Kelas Desil ke {d} (fD) = {fd}"],
                [
                    f"Frek. Kumulatif sebelum Kelas Desil ke {d} = {prev_cumulative_freq} → s = {letak_desil} - {prev_cumulative_freq} = {s}"
                ],
                [
                    f"Frek. Kumulatif sampai Kelas Desil ke {d} = {cumulative_freq} → s’ = {cumulative_freq} - {letak_desil} = {s_}"
                ],
                [
                    f"TBB Kelas Desil ke {d} + i(s/fd)\n"
                    f"= {TBB} + {interval}({s}/{fd:.1f})\n"
                    f"= {TBB} + {interval * (s / fd):.1f} = {desil:.2f}"
                ],
                [
                    f"TBA Kelas Desil ke {d} - i(s'/fd)\n"
                    f"= {TBA} - {interval}({s_}/{fd:.1f})\n"
                    f"= {TBA} - {interval * (s_ / fd):.1f} = {desil:.2f}"
                ],
            ],
            tablefmt="rounded_grid",
        )
    )
    print()

    print("Persentil ke - p:")
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

    print(
        tabulate(
            [
                [f"Letak Persentil ke {p} = {p} x {n}/100 = {letak_persentil}"],
                [f"Kelas Persentil ke {p} = {kelas_persentil}"],
                [
                    f"TBB Kelas Persentil ke {p} = {TBB} | TBA Kelas Persentil ke {p} = {TBA}"
                ],
                [f"Frekuensi Kelas Persentil ke {p} (fP) = {fp}"],
                [
                    f"Frek. Kumulatif sebelum Kelas Persentil ke {p} = {prev_cumulative_freq} → s = {letak_persentil} - {prev_cumulative_freq} = {s}"
                ],
                [
                    f"Frek. Kumulatif sampai Kelas Persentil ke {p} = {cumulative_freq} → s’ = {cumulative_freq} - {letak_persentil} = {s_}"
                ],
                [
                    f"TBB Kelas Persentil ke {p} + i(s/fp)\n"
                    f"= {TBB} + {interval}({s}/{fp:.1f})\n"
                    f"= {TBB} + {interval * (s / fp):.1f} = {persentil:.2f}"
                ],
                [
                    f"TBA Kelas Persentil ke {p} - i(s'/fp)\n"
                    f"= {TBA} - {interval}({s_}/{fp:.1f})\n"
                    f"= {TBA} - {interval * (s_ / fp):.1f} = {persentil:.2f}"
                ],
            ],
            tablefmt="rounded_grid",
        )
    )
    print()


if __name__ == "__main__":
    main()
