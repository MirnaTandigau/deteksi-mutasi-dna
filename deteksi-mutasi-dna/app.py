from flask import Flask, render_template, request

app = Flask(__name__)

def highlight_seq(ref, pasien):
    ref_out = ""
    pasien_out = ""
    max_len = max(len(ref), len(pasien))

    for i in range(max_len):
        r = ref[i] if i < len(ref) else "-"
        p = pasien[i] if i < len(pasien) else "-"

        if r != p:
            ref_out += f"<span style='background-color:yellow;font-weight:bold'>{r}</span>"
            pasien_out += f"<span style='background-color:yellow;font-weight:bold'>{p}</span>"
        else:
            ref_out += r
            pasien_out += p
    return ref_out, pasien_out

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = ""
    dna_ref = ""
    dna_pasien = ""
    if request.method == "POST":
        dna_ref = request.form.get("dnaRef", "").strip().upper()
        dna_pasien = request.form.get("dnaPasien", "").strip().upper()

        stats = {
            "total": max(len(dna_ref), len(dna_pasien)),
            "mutasi": 0,
            "substitusi": 0,
            "delesi": 0,
            "insersi": 0
        }

        tabel = []
        panjang = min(len(dna_ref), len(dna_pasien))

        for i in range(panjang):
            if dna_ref[i] != dna_pasien[i]:
                tabel.append({
                    "pos": i+1,
                    "tipe": "Substitusi",
                    "ref": dna_ref[i],
                    "pasien": dna_pasien[i]
                })
                stats["mutasi"] += 1
                stats["substitusi"] += 1

        if len(dna_ref) > len(dna_pasien):
            stats["mutasi"] += 1
            stats["delesi"] += 1
            tabel.append({
                "pos": len(dna_pasien)+1,
                "tipe": "Delesi",
                "ref": dna_ref[len(dna_pasien):],
                "pasien": "-"
            })
        elif len(dna_pasien) > len(dna_ref):
            stats["mutasi"] += 1
            stats["insersi"] += 1
            tabel.append({
                "pos": len(dna_ref)+1,
                "tipe": "Insersi",
                "ref": "-",
                "pasien": dna_pasien[len(dna_ref):]
            })

        ref_out, pasien_out = highlight_seq(dna_ref, dna_pasien)

        hasil = {
            "stats": stats,
            "tabel": tabel,
            "ref_out": ref_out,
            "pasien_out": pasien_out,
        }

    return render_template("index.html", hasil=hasil, dna_ref=dna_ref, dna_pasien=dna_pasien)

if __name__ == "__main__":
    app.run(debug=True)
