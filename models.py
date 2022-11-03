import pymysql
import config2

db = cursor = None

class MModel:
	def __init__ (self, no=None, nama=None, no_telp=None):
		self.no = no
		self.nama = nama
		self.no_telp = no_telp
		
	def openDB(self):
		global db, cursor
		db = pymysql.connect(
			host=config2.DB_HOST,
			user=config2.DB_USER,
			password=config2.DB_PASSWORD,
			database=config2.DB_NAME)
		cursor = db.cursor()

	def closeDB(self):
		global db, cursor
		db.close()

	# validasi login dengan table data_pengguna.
	def authenticate(self, username=None, password=None):
		self.openDB()
		cursor.execute("SELECT COUNT(*) FROM data_pengguna WHERE username = '%s' AND password = MD5('%s')" % (username, password))
		count_account = (cursor.fetchone())[0]
		self.closeDB()
		return True if count_account>0 else False
# ========================================= pengguna ============================================
	# menampilkan data pengguna oleh admin.
	def selectPengguna(self):
		self.openDB()
		cursor.execute("SELECT pengguna_id, username, password, tipe_pengguna, pengguna_nama FROM `data_pengguna`")
		container = []
		for pengguna_id, username, password, tipe_pengguna, pengguna_nama in cursor.fetchall():
			container.append((pengguna_id, username, password, tipe_pengguna, pengguna_nama))
		self.closeDB()
		return container

	def getUserForSession(self, username):
		self.openDB()
		cursor.execute("SELECT username, pengguna_nama, tipe_pengguna FROM data_pengguna WHERE username='%s'" % username)
		data_nama = cursor.fetchone()
		return data_nama

	# tambah data pengguna.
	def insertPengguna(self, data_p):
		self.openDB()
		cursor.execute("INSERT INTO data_pengguna (pengguna_id, username, password, tipe_pengguna, pengguna_nama) VALUES('%s', '%s', MD5('%s'), '%s', '%s')" % data_p)
		db.commit()
		self.closeDB()

	# edit / update data pengguna.
	def updatePengguna(self, data_pg):
		self.openDB()
		cursor.execute("UPDATE data_pengguna SET username='%s', password='%s', tipe_pengguna='%s', pengguna_nama='%s' WHERE pengguna_id='%s'" % data_pg)
		db.commit()
		self.closeDB()

	def getUserbyNo(self, pengguna_id):
		self.openDB()
		cursor.execute("SELECT pengguna_id, username, password, tipe_pengguna, pengguna_nama FROM data_pengguna WHERE pengguna_id='%s'" % pengguna_id)
		data_pg = cursor.fetchone()
		return data_pg

	# hapus data pengguna.
	def deletePengguna(self, pengguna_id):
		self.openDB()
		cursor.execute("DELETE FROM data_pengguna WHERE pengguna_id='%s'" % pengguna_id)
		db.commit()
		self.closeDB()

	# menampilkan profil pengguna yang login.
	def selectProfilPengguna(self):
		self.openDB()
		cursor.execute("SELECT * FROM `data_pengguna`")
		pp = []
		for pengguna_id, username, password, tipe_pengguna, pengguna_nama in cursor.fetchall():
			pp.append((pengguna_id, username, password, tipe_pengguna,pengguna_nama))
		self.closeDB()
		return pp

# ========================================= Laporan ============================================

	# menampilkan laporan.
	def selectLaporan(self):
		self.openDB()
		cursor.execute("SELECT no, username, mata_pelajaran, tanggal_lapor, tanggal_proses, status FROM data_laporan")
		container_lp = []
		for no, username, mata_pelajaran, tanggal_lapor, tanggal_proses, status in cursor.fetchall():
			container_lp.append((no, username, mata_pelajaran, tanggal_lapor, tanggal_proses, status))
		self.closeDB()
		return container_lp

	# tambah data laporan.
	def insertLaporan(self, data_lp):
		self.openDB()
		cursor.execute("INSERT INTO data_laporan (no, username, mata_pelajaran, tanggal_lapor, tanggal_proses, status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % data_lp)
		db.commit()
		self.closeDB()

	# def getLaporForSession(self, username):
	# 	self.openDB()
	# 	cursor.execute("SELECT username, mata_pelajaran, hari, tanggal, status FROM data_laporan WHERE username='%s'" % username)
	# 	data_nama = cursor.fetchone()
	# 	return data_nama

	# edit / update data laporan.
	def updateLaporan(self, data_lp):
		self.openDB()
		cursor.execute("UPDATE data_laporan SET username='%s', mata_pelajaran='%s', tanggal_lapor='%s', tanggal_proses='%s', status='%s' WHERE no=%s" % data_lp)
		db.commit()
		self.closeDB()

	def getLaporbyNo(self, no):
		self.openDB()
		cursor.execute("SELECT no, username, mata_pelajaran, tanggal_lapor, tanggal_proses, status FROM data_laporan WHERE no=%s" % no)
		data_lp = cursor.fetchone()
		return data_lp

# ========================================= Keluhan ============================================

	# menampilkan laporan.
	def selectKeluhan(self):
		self.openDB()
		cursor.execute("SELECT no, username, keluhan, laporan_masuk, laporan_diterima, status FROM data_keluhan")
		container_kl = []
		for no, username, keluhan, laporan_masuk, laporan_diterima, status in cursor.fetchall():
			container_kl.append((no, username, keluhan, laporan_masuk, laporan_diterima, status))
		self.closeDB()
		return container_kl

	# tambah data laporan.
	def insertKeluhan(self, data_kl):
		self.openDB()
		cursor.execute("INSERT INTO data_keluhan (no, username, keluhan, laporan_masuk, laporan_diterima, status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % data_kl)
		db.commit()
		self.closeDB()

	# def getKeluhanForSession(self, username):
	# 	self.openDB()
	# 	cursor.execute("SELECT username, keluhan, laporan_masuk, laporan_diterima, status FROM data_keluhan WHERE username='%s'" % username)
	# 	data_nama = cursor.fetchone()
	# 	return data_nama

	# edit / update data laporan.
	def updateKeluhan(self, data_kl):
		self.openDB()
		cursor.execute("UPDATE data_keluhan SET username='%s', keluhan='%s', laporan_masuk='%s', laporan_diterima='%s', status='%s' WHERE no=%s" % data_kl)
		db.commit()
		self.closeDB()

	def getKeluhanbyNo(self, no):
		self.openDB()
		cursor.execute("SELECT no, username, keluhan, laporan_masuk, laporan_diterima, status FROM data_keluhan WHERE no=%s" % no)
		data_kl = cursor.fetchone()
		return data_kl