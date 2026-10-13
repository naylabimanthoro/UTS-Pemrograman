from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "kunci_rahasia_nayla"
# Menggunakan SQLite agar data tersimpan secara permanen
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mahasiswa.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Struktur Tabel Mahasiswa[cite: 1]
class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.Integer, unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    program_studi = db.Column(db.String(100), nullable=False)
    angkatan = db.Column(db.Integer, nullable=False)
    ipk = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    mahasiswa = Mahasiswa.query.all()
    tahun_sekarang = datetime.now().year
    return render_template('index.html', mahasiswa=mahasiswa, tahun_sekarang=tahun_sekarang)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        program_studi = request.form['program_studi']
        angkatan = request.form['angkatan']
        ipk = request.form['ipk']

        # Validasi field kosong[cite: 1]
        if not nim or not nama or not program_studi or not angkatan or not ipk:
            flash('Semua field wajib diisi!', 'danger')
            return redirect(url_for('add'))

        try:
            ipk = float(ipk)
            # Validasi IPK[cite: 1]
            if ipk < 0.00 or ipk > 4.00:
                flash('IPK harus berada di rentang 0.00 - 4.00!', 'danger')
                return redirect(url_for('add'))
        except ValueError:
            flash('IPK harus berupa angka!', 'danger')
            return redirect(url_for('add'))

        # Validasi NIM duplikat
        cek_nim = Mahasiswa.query.filter_by(nim=nim).first()
        if cek_nim:
            flash('NIM sudah terdaftar!', 'danger')
            return redirect(url_for('add'))

        mhs_baru = Mahasiswa(nim=nim, nama=nama, program_studi=program_studi, angkatan=angkatan, ipk=ipk)
        db.session.add(mhs_baru)
        db.session.commit()
        flash('Data berhasil ditambahkan!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    mhs = Mahasiswa.query.get_or_404(id)
    if request.method == 'POST':
        mhs.nama = request.form['nama']
        mhs.program_studi = request.form['program_studi']
        mhs.angkatan = request.form['angkatan']
        ipk = request.form['ipk']

        if not mhs.nama or not mhs.program_studi or not mhs.angkatan or not ipk:
            flash('Semua field wajib diisi!', 'danger')
            return redirect(url_for('edit', id=id))

        try:
            mhs.ipk = float(ipk)
            if mhs.ipk < 0.00 or mhs.ipk > 4.00:
                flash('IPK harus berada di rentang 0.00 - 4.00!', 'danger')
                return redirect(url_for('edit', id=id))
        except ValueError:
            flash('IPK harus berupa angka!', 'danger')
            return redirect(url_for('edit', id=id))

        db.session.commit()
        flash('Data berhasil diubah!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', mhs=mhs)

@app.route('/delete/<int:id>')
def delete(id):
    mhs = Mahasiswa.query.get_or_404(id)
    db.session.delete(mhs)
    db.session.commit()
    flash('Data berhasil dihapus!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)