from flask import Flask, request, jsonify, render_template, json, redirect, redirect, url_for, session, make_response
from flask_mongoengine import MongoEngine #ModuleNotFoundError: No module named 'flask_mongoengine' = (venv) C:\flaskmyproject>pip install flask-mongoengine
from datetime import datetime
from models import MModel
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, \
    TimeoutException, ElementNotInteractableException
from time import sleep
from database import dbBrainly
from pymongo import MongoClient

import pymongo
import datetime
import config2
import config

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["brainlydb"]

application = Flask(__name__)
application.config['SECRET_KEY'] = 'sfh7^erw9*(%sadHGw%R'

# today = datetime.today()
model = MModel()
html_source = ''
 
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'brainlydb',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

# RIWAYAT PENGGUNA
@application.route('/profil_pengguna/<mapel>')
def profil_pengguna(mapel):
    if 'data_nama' in session:
        # current_time_date = today.strftime("%B %d, %Y")
        data_nama = session['data_nama']
        mycol = mydb[mapel]
        myquery = { "penjawab": data_nama[0] , "mapel": mapel}  
        container = mycol.find(myquery)
        mapel = mapel.capitalize()
        return render_template('data_soal.html', mapel=mapel, data_nama=data_nama, container=container)
    return render_template('form_login.html')

# CEK DATA SOAL
@application.route('/cek_data_soal/<mapel>')
def cek_data_soal(mapel):
    if 'data_nama' in session:
        # current_time_date = today.strftime("%B %d, %Y")
        data_nama = session['data_nama']
        mycol = mydb[mapel]
        mydoc = { "terjawab": False}
        jumlah = mycol.count_documents(mydoc)
        print("Soal yang belum dijawab pada mata pelajaran", mapel) 
        print("berjumlah", jumlah)
        mydocs = { "terverifikasi": False}
        total = mycol.count_documents(mydocs)
        print("Soal yang belum diverifikasi pada mata pelajaran", mapel) 
        print("berjumlah", total)
        mapel = mapel.capitalize()
        container=mycol.find()
        mapel = mapel.upper()
        if mapel == 'BAHASA INDONESIA':
            kode_mapel = 0
        elif mapel == 'BAHASA INGGRIS': 
            kode_mapel = 1
        elif mapel == 'BIOLOGI': 
            kode_mapel = 2
        elif mapel == 'EKONOMI': 
            kode_mapel = 3
        elif mapel == 'FISIKA': 
            kode_mapel = 4
        elif mapel == 'GEOGRAFI': 
            kode_mapel = 5
        elif mapel == 'KIMIA': 
            kode_mapel = 6
        elif mapel == 'MATEMATIKA': 
            kode_mapel = 7
        elif mapel == 'PPKN': 
            kode_mapel = 8
        elif mapel == 'PENJASKES': 
            kode_mapel = 9
        elif mapel == 'SEJARAH': 
            kode_mapel = 10
        elif mapel == 'SENI': 
            kode_mapel = 11
        elif mapel == 'SOSIOLOGI': 
            kode_mapel = 12
        else:
            kode_mapel = 13
        return render_template('data_soal.html', kode_mapel=kode_mapel, mapel=mapel, jumlah=jumlah, total=total, data_nama=data_nama, container=container)
    return render_template('form_login.html')
# ============================================================================================================  
# Index
@application.route('/')
def index():
	if 'data_nama' in session:
		# current_time_date = today.strftime("%B %d, %Y")
		data_nama = session['data_nama']
		return render_template('index.html', data_nama=data_nama)
	return render_template('form_login.html')

# login	
@application.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if model.authenticate(username, password):
			data_nama = model.getUserForSession(username)
			session['data_nama'] = data_nama
			return redirect(url_for('index'))
		msg = 'Username/Password salah.'
		return render_template('form_login.html', msg=msg)
	return render_template('form_login.html')

# Logout	
@application.route('/logout')
def logout():
	session.pop('data_nama', '')
	return redirect(url_for('index'))
# ================================ MASTER BARANG ================================

# @application.route('/masterbarang')
# def masterbarang():
#     if 'data_nama' in session:
#         data_nama = session['data_nama']
#         username = data_nama[1]
#         con_barang = [] 
#         con_barang = model.selectMasterBarang()
#         return render_template('masterbarang.html', con_barang=con_barang, data_nama=data_nama)
#     return render_template('form_login.html')

# @application.route('/insert_master_barang', methods=['GET', 'POST'])
# def insert_master_barang():
# 	if 'data_nama' in session:
# 		if request.method == 'POST':
# 			nama = request.form['nama']
# 			harga = request.form['harga']
# 			satuan = request.form['satuan']
# 			data_master_barang = (nama, harga, satuan)
# 			model.insertMasterBarang(data_master_barang)
# 			return redirect(url_for('masterbarang'))
# 		else:
# 			data_nama = session['data_nama']
# 			return render_template('insert_master_barang.html', data_nama=data_nama)
# 	return render_template('form_login.html')

    
# ======================================= pengguna ================================

@application.route('/pengguna')
def pengguna():
    if 'data_nama' in session:
        data_nama = session['data_nama']
        username = data_nama[1]
        container = [] 
        container = model.selectPengguna()
        return render_template('pengguna.html', container=container, data_nama=data_nama)
    return render_template('form_login.html')

# menambahkan data pengguna.
@application.route('/insert_pengguna', methods=['GET', 'POST'])
def insert_pengguna():
	if 'data_nama' in session:
		if request.method == 'POST':
			pengguna_id = request.form['pengguna_id']
			username = request.form['username']
			password = request.form['password']
			tipe_pengguna = request.form['tipe_pengguna']
			pengguna_nama = request.form['pengguna_nama']
			data_p = (pengguna_id, username, password, tipe_pengguna, pengguna_nama)
			model.insertPengguna(data_p)
			return redirect(url_for('pengguna'))
		else:
			data_nama = session['data_nama']
			return render_template('insert_pengguna.html', data_nama=data_nama)
	return render_template('form_login.html')

# edit / update data pengguna.
@application.route('/update_pg', methods=['GET', 'POST'])
def update_pg():
	if 'data_nama' in session:
		pengguna_id = request.form['pengguna_id']
		username = request.form['username']
		password = request.form['password']
		tipe_pengguna = request.form['tipe_pengguna']
		pengguna_nama = request.form['pengguna_nama']
		data_pg = (username, password, tipe_pengguna, pengguna_nama, pengguna_id)
		model.updatePengguna(data_pg)
		return redirect(url_for('pengguna'))
	return render_template('form_login.html')

@application.route('/update_pengguna/<pengguna_id>')
def update_pengguna(pengguna_id):
	if 'data_nama' in session:
		data_pg = model.getUserbyNo(pengguna_id)
		data_nama = session['data_nama']
		return render_template('edit_pengguna.html', data_pg=data_pg, data_nama=data_nama)
	return redirect(url_for('login')) 

# menghapus data pengguna.
@application.route('/delete_pengguna/<pengguna_id>')
def delete_pengguna(pengguna_id):
	if 'data_nama' in session:
		model.deletePengguna(pengguna_id)
		return redirect(url_for('pengguna'))
	return render_template('form_login.html')

# ======================================= Data Soal ================================

# menampilkan data soal.
@application.route('/data_soal')
def data_soal():
	if 'data_nama' in session:
		# current_time_date = today.strftime("%B %d, %Y")
		data_nama = session['data_nama']
		if data_nama[2] == 0:
			return render_template('index.html', data_nama=data_nama)
		else:
			return redirect(url_for('index'))
	return render_template('form_login.html')

# menampilkan ketersediaan soal.
@application.route('/update_soal/<kode_mapel>')
def update_soal(kode_mapel):
    kode_mapel = int(kode_mapel)
    if kode_mapel == 0:
        nama_col = 'bahasa indonesia'
    elif kode_mapel == 1: 
        nama_col = 'bahasa inggris'
    elif kode_mapel == 2: 
        nama_col = 'biologi'
    elif kode_mapel == 3: 
        nama_col = 'ekonomi'
    elif kode_mapel == 4: 
        nama_col = 'fisika'
    elif kode_mapel == 5: 
        nama_col = 'geografi'
    elif kode_mapel == 6: 
        nama_col = 'kimia'
    elif kode_mapel == 7: 
        nama_col = 'matematika'
    elif kode_mapel == 8: 
        nama_col = 'penjaskes'
    elif kode_mapel == 9: 
        nama_col = 'ppkn'
    elif kode_mapel == 10: 
        nama_col = 'sejarah'
    elif kode_mapel == 11: 
        nama_col = 'seni'
    elif kode_mapel == 12: 
        nama_col = 'sosiologi'
    else:
        nama_col = 'ti'

    def get_browser():
        opts = Options()
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--no-sandbox")
        driver = Chrome(executable_path=r'D:/MY_FLASK/User/Adji/chromedriver.exe', options=opts)
        return driver

    def check_pop_up(driver):
        pop_up_elem = '/html/body/div[2]/div/div[3]'
        driver.implicitly_wait(5)
        try:
            driver.find_element_by_xpath(pop_up_elem).click()
            print('udah di close')
        except NoSuchElementException:
            print('tidak muncul')
            pass
        except ElementNotInteractableException:
            print('tidak ada popup')
            pass

    def get_info(driver, url):
        driver.get(url)
        sleep(3)
        check_pop_up(driver)


    # Text Pertanyaan
        try:
            text_elem = '/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/article/div/div/div[2]/div/div/h1'
            text = driver.find_element_by_xpath(text_elem).text
        except NoSuchElementException:
            text = ''

        # Penjawab
        try:
            penjawab_elem = '//*[@id="question-sg-layout-container"]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/span'
            penjawab = driver.find_element_by_xpath(penjawab_elem).text
        except NoSuchElementException:
            penjawab = ''

        # Status Terjawab
        try:
            button_style = 'span.sg-button__text'
            content = driver.find_element_by_id('question-sg-layout-container')
            span_text = content.find_element_by_css_selector(button_style).text

            if 'LIHAT JAWABAN' in span_text:
                terjawab = True
            else:
                terjawab = False

        except NoSuchElementException:
            terjawab = ''

        # Jawaban terverifikasi
        try:
            verif_elem = '/html/body/div[5]/div/div[4]/div[1]/div[1]/div[4]/div/div[1]/div/div[1]/div/div[1]/div[2]/h3'
            verif = driver.find_element_by_tag_name("h3").text
            if 'Jawaban terverifikasi ahli' in verif:
                terverifikasi = True
            else:
                terverifikasi = False

        except NoSuchElementException:
            terverifikasi = ''

        data = {
            'url': url,
            'text_soal': text,
            'penjawab': penjawab,
            'terjawab': terjawab,
            'terverifikasi': terverifikasi
            }
        return data

    def get_subject_links(driver):
        driver.implicitly_wait(5)
        xpath_load = '//*[@id="loadMore"]'
        for i in range(10):
            driver.find_element_by_xpath(xpath_load).click()
            sleep(3)
            print('load ke {}'.format(i))
        questions = driver.find_elements_by_xpath('/html/body/div[6]/div/div[2]/div[3]/div')
        href_list = []
        i = 1
        for q in questions:
            xpath_answer = '//*[@id="questions"]/div[{}]/div/div/div/a'.format(i)
            href = q.find_element_by_xpath(xpath_answer).get_attribute('href')
            href_list.append(href)
            i+=1
        return href_list

    db = dbBrainly('brainlydb')
    driver = get_browser()

    data_mapel = config.MAPEL[kode_mapel]
    # GET URL
    url = 'https://id.brainly.vip/unanswered/{}.html'.format(data_mapel)

    driver.get(url)
    links = get_subject_links(driver)
    print('scraping for details....')
    for url in links:
        try:
            collected = get_info(driver, url)
            collected['mapel'] = nama_col
            db.insert_info(nama_col, collected)
            print('data {} inserted'.format(data_mapel))
            sleep(3)

        except NoSuchElementException as no_element:
            print(no_element)
            pass
    print('done')
    return redirect(url_for('index'))
# ======================================= menampilkan laporan ================================

@application.route('/laporan')
def laporan():
    if 'data_nama' in session:
        container_lp = []
        container_lp = model.selectLaporan()
        data_nama = session['data_nama']
        return render_template('laporan.html', container_lp=container_lp, data_nama=data_nama)
    return render_template('form_login.html')

# tambah laporan.
@application.route('/insert_laporan', methods=['GET', 'POST'])
def insert_laporan():
    if 'data_nama' in session:
        if request.method == 'POST':
            no = request.form['no']
            username = request.form['username']
            mata_pelajaran = request.form['mata_pelajaran']
            tanggal_lapor = datetime.datetime.now()
            tanggal_proses = 0
            status = None
            data_lp = (no, username, mata_pelajaran, tanggal_lapor, tanggal_proses, status)
            model.insertLaporan(data_lp)
            return redirect(url_for('laporan'))
        else:
            data_nama = session['data_nama']
            return render_template('tambah_laporan.html', data_nama=data_nama)
    return render_template('form_login.html')

# proses edit / update data laporan.
@application.route('/update_lp', methods=['GET', 'POST'])
def update_lp():
    if 'data_nama' in session:
        pengguna_id = request.form['pengguna_id']
        username = request.form['username']
        mata_pelajaran = request.form['mata_pelajaran']
        tanggal_lapor = datetime.datetime.now()
        tanggal_proses = datetime.datetime.now()
        status = request.form['status']
        data_lp = (username, mata_pelajaran, tanggal_lapor, tanggal_proses, status, pengguna_id)
        model.updateLaporan(data_lp)
        return redirect(url_for('laporan'))
    return render_template('form_login.html')

# edit / update data laporan.
@application.route('/update_laporan/<no>')
def update_laporan(no):
    if 'data_nama' in session:
        data_lp = model.getLaporbyNo(no)
        data_nama = session['data_nama']
        return render_template('edit_laporan.html', data_lp=data_lp, data_nama=data_nama)
    return render_template('form_login.html')

# ======================================= menampilkan laporan ================================

@application.route('/keluhan')
def keluhan():
    if 'data_nama' in session:
        container_kl = []
        container_kl = model.selectKeluhan()
        data_nama = session['data_nama']
        return render_template('keluhan.html', container_kl=container_kl, data_nama=data_nama)
    return render_template('form_login.html')

# tambah keluhan.
@application.route('/insert_keluhan', methods=['GET', 'POST'])
def insert_keluhan():
    if 'data_nama' in session:
        if request.method == 'POST':
            no = request.form['no']
            username = request.form['username']
            keluhan = request.form['keluhan']
            laporan_masuk = datetime.datetime.now()
            laporan_diterima = 0
            status = 0
            data_kl = (no, username, keluhan, laporan_masuk, laporan_diterima, status)
            model.insertKeluhan(data_kl)
            return redirect(url_for('keluhan'))
        else:
            data_nama = session['data_nama']
            return render_template('tambah_keluhan.html', data_nama=data_nama)
    return render_template('form_login.html')

# proses edit / update data keluhan.
@application.route('/update_kl', methods=['GET', 'POST'])
def update_kl():
    if 'data_nama' in session:
        no = request.form['no']
        username = request.form['username']
        keluhan = request.form['keluhan']
        laporan_masuk = datetime.datetime.now()
        laporan_diterima = datetime.datetime.now()
        status = request.form['status']
        data_kl = (username, keluhan, laporan_masuk, laporan_diterima, status, no)
        model.updateKeluhan(data_kl)
        return redirect(url_for('keluhan'))
    return render_template('form_login.html')

# edit / update data keluhan.
@application.route('/update_keluhan/<no>')
def update_keluhan(no):
    if 'data_nama' in session:
        data_kl = model.getKeluhanbyNo(no)
        data_nama = session['data_nama']
        return render_template('edit_keluhan.html', data_kl=data_kl, data_nama=data_nama)
    return render_template('form_login.html')

if __name__ == '__main__':
    application.run(debug=True)