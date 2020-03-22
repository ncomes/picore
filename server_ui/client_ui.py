#! /usr/bin/python3
import sys
main_path = r'/home/pi/picore'
sys.path.append(main_path)

import datetime
import python_core.json_data as json_data
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import os
import time
import server_ui.multi_client as mc
import server_ui.shutdown_client as sc




HOSTS = ['192.168.86.243']
PORT = 5560

CAM_JSON = 'hosts_and_port'
FACE_POSES_JSON = 'face_poses'
CAM_JSON_PATH = os.path.join(main_path, 'json')
PHOTO_PATH = r'/home/pi/pictures'
MEDIA_PATH = r'/media/pi/Elements'

class MultiServerCaptureUI(QtGui.QWidget):
	def __init__(self):
		super(MultiServerCaptureUI, self).__init__()
		self.init_ui()
	
	def init_ui(self):
		self.setGeometry(600, 600, 250, 150)
		self.setWindowTitle('Pi Cam Photo Server')
		self.resize(500, 600)
		
		self.main_v_layout = QtGui.QVBoxLayout()
		self.main_v_layout.setSpacing(5)
		self.main_v_layout.setAlignment(QtCore.Qt.AlignTop)
		self.setLayout(self.main_v_layout)
		
		# Menu bar
		# menu Servers
		self.menu_bar = QtGui.QMenuBar(parent=self)
		self.servers = QtGui.QMenu(self)
		self.servers.setTitle('Servers')
		self.menu_bar.addMenu(self.servers)

		# menu Git
		self.update_servers = QtGui.QMenu(self)
		self.update_servers.setTitle('Git')
		self.menu_bar.addMenu(self.update_servers)

		# menu Power Options
		self.pwr_opt_menu = QtGui.QMenu(self)
		self.pwr_opt_menu.setTitle('Power Options')
		self.menu_bar.addMenu(self.pwr_opt_menu)

		# Server Actions
		self.kill_all_menu = QtGui.QAction('Stop All', self)
		self.kill_all_menu.triggered.connect(self.kill_all)
		self.kill_all_menu.setStatusTip('Stops all the Raspberry Pi Servers.')
		self.servers.addAction(self.kill_all_menu)
		
		self.kill_one_menu = QtGui.QAction('Stop Selected', self)
		self.kill_one_menu.triggered.connect(self.kill_one)
		self.kill_one_menu.setToolTip('Stops Raspberry Pi Server with the selected IP Address.')
		self.servers.addAction(self.kill_one_menu)

		# Git Actions
		self.update_servers_all = QtGui.QAction('Python Update All', self)
		self.update_servers_all.triggered.connect(self.update_all)
		self.update_servers_all.setStatusTip('Stops all the Raspberry Pi Servers.')
		self.update_servers.addAction(self.update_servers_all)
		
		self.update_one_menu = QtGui.QAction('Python Update Selected', self)
		self.update_one_menu.triggered.connect(self.update_one)
		self.update_one_menu.setToolTip('Stops Raspberry Pi Server with the selected IP Address.')
		self.update_servers.addAction(self.update_one_menu)

		# Power Actions
		self.shutdown_all_menu = QtGui.QAction('Shutdown All', self)
		self.shutdown_all_menu.triggered.connect(self.shutdown_all)
		self.shutdown_all_menu.setStatusTip('Turns off all the Raspberry Pi Servers.')
		self.pwr_opt_menu.addAction(self.shutdown_all_menu)

		self.shutdown_one_menu = QtGui.QAction('Shutdown Selected', self)
		self.shutdown_one_menu.triggered.connect(self.shutdown_one)
		self.shutdown_one_menu.setToolTip('Turns off the Raspberry Pi Server with the selected IP Address.')
		self.pwr_opt_menu.addAction(self.shutdown_one_menu)

		self.reboot_all_menu = QtGui.QAction('Reboot All', self)
		self.reboot_all_menu.triggered.connect(lambda : self.reboot_now(all=True))
		self.reboot_all_menu.setStatusTip('Turns off all the Raspberry Pi Servers.')
		self.pwr_opt_menu.addAction(self.reboot_all_menu)

		self.reboot_one_menu = QtGui.QAction('Reboot Selected', self)
		self.reboot_one_menu.triggered.connect(lambda : self.reboot_now(all=False))
		self.reboot_one_menu.setToolTip('Turns off the Raspberry Pi Server with the selected IP Address.')
		self.pwr_opt_menu.addAction(self.reboot_one_menu)

		self.main_v_layout.addWidget(self.menu_bar)
		
		### Main Layout ###
		
		self.main_h_spacer_layout = QtGui.QHBoxLayout()
		self.main_h_spacer_layout.setSpacing(25)
		self.main_h_spacer_layout.setAlignment(QtCore.Qt.AlignTop)
		self.main_v_layout.addLayout(self.main_h_spacer_layout)
		
		self.main_h_layout = QtGui.QHBoxLayout()
		self.main_h_layout.setSpacing(5)
		self.main_h_layout.setAlignment(QtCore.Qt.AlignTop)
		self.main_v_layout.addLayout(self.main_h_layout)
		
		self.main_layout = QtGui.QVBoxLayout()
		self.main_layout.setSpacing(5)
		self.main_layout.setAlignment(QtCore.Qt.AlignTop)
		self.main_h_layout.addLayout(self.main_layout)
		
		# port line edit
		self.port_layout = QtGui.QHBoxLayout()
		self.main_layout.addLayout(self.port_layout)
		
		self.port_label = QtGui.QLabel('Port Number: ')
		self.port_layout.addWidget(self.port_label)
		
		self.port_lineEdit = QtGui.QLineEdit()
		self.port_layout.addWidget(self.port_lineEdit)
		
		# ip address list widget
		self.ip_label = QtGui.QLabel('IP Addresses: ')
		self.main_layout.addWidget(self.ip_label)
		
		self.list_widget_layout = QtGui.QHBoxLayout()
		self.list_widget_layout.setSpacing(5)
		self.list_widget_layout.setAlignment(QtCore.Qt.AlignTop)
		self.main_layout.addLayout(self.list_widget_layout)
		
		self.host_listWidget = QtGui.QListWidget()
		self.list_widget_layout.addWidget(self.host_listWidget)
		self.host_listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.sel_host = self.host_listWidget.selectionModel()
		
		# line Edit for ip address
		self.add_ip_layout = QtGui.QHBoxLayout()
		self.main_layout.addLayout(self.add_ip_layout)
		
		self.ip_lineEdit = QtGui.QLineEdit()
		self.add_ip_layout.addWidget(self.ip_lineEdit)
		
		# button to add and remove ip addresses
		self.add_host_layout = QtGui.QHBoxLayout()
		self.main_layout.addLayout(self.add_host_layout)
		
		self.add_host_pushButton = QtGui.QPushButton('Add IP Address')
		self.add_host_layout.addWidget(self.add_host_pushButton)
		
		self.remove_host_pushButton = QtGui.QPushButton('Remove IP Address')
		self.add_host_layout.addWidget(self.remove_host_pushButton)
		
		self.replace_host_pushButton = QtGui.QPushButton('Replace IP Address')
		self.add_host_layout.addWidget(self.replace_host_pushButton)
		
		# v spacer
		self.main_spacer_layout = QtGui.QVBoxLayout()
		self.main_spacer_layout.setSpacing(5)
		self.main_h_layout.addLayout(self.main_spacer_layout)
		
		self.spacer_label = QtGui.QLabel('')
		self.spacer_label.setFixedWidth(10)
		self.main_spacer_layout.addWidget(self.spacer_label)
		
		# capture - take the photo!
		self.main_capture_layout = QtGui.QVBoxLayout()
		self.main_capture_layout.setSpacing(5)
		self.main_capture_layout.setAlignment(QtCore.Qt.AlignTop)
		self.main_h_layout.addLayout(self.main_capture_layout)
		
		self.capture_label = QtGui.QLabel('Pose Names: ')
		self.main_capture_layout.addWidget(self.capture_label)
		
		self.pose_list_layout = QtGui.QHBoxLayout()
		self.pose_list_layout.setSpacing(5)
		self.pose_list_layout.setAlignment(QtCore.Qt.AlignTop)
		self.main_capture_layout.addLayout(self.pose_list_layout)
		
		self.poses_listWidget = QtGui.QListWidget()
		self.poses_listWidget.setMinimumWidth(300)
		self.main_capture_layout.addWidget(self.poses_listWidget)
		
		self.pose_lineEdit = QtGui.QLineEdit()
		self.main_capture_layout.addWidget(self.pose_lineEdit)
		
		self.add_poses_layout = QtGui.QHBoxLayout()
		self.main_capture_layout.addLayout(self.add_poses_layout)
		
		self.add_pose_pushButton = QtGui.QPushButton('Add Pose')
		self.add_poses_layout.addWidget(self.add_pose_pushButton)
		
		self.remove_pose_pushButton = QtGui.QPushButton('Remove Pose')
		self.add_poses_layout.addWidget(self.remove_pose_pushButton)
		
		# take photos
		self.capture_label = QtGui.QLabel('Capture - Take Photos: ')
		self.main_capture_layout.addWidget(self.capture_label)
		
		self.pic_btn_layout = QtGui.QHBoxLayout()
		self.pic_btn_layout.setAlignment(QtCore.Qt.AlignTop)
		self.main_capture_layout.addLayout(self.pic_btn_layout)
		
		self.pic_button = QtGui.QPushButton('Capture')
		self.pic_btn_layout.addWidget(self.pic_button)

		self.pic_sel_button = QtGui.QPushButton('Capture With Selected')
		self.pic_btn_layout.addWidget(self.pic_sel_button)
		
		# populate information
		hosts, port = get_hosts_and_port()
		if hosts and port:
			self.host_listWidget.addItems(hosts)
			self.port_lineEdit.setText(str(port))
		else:
			self.host_listWidget.addItems(HOSTS)
			self.port_lineEdit.setText(str(PORT))
		self.host_listWidget.setCurrentRow(0)
			
		pose_names = import_pose_names()
		if pose_names:
			self.poses_listWidget.addItems(pose_names)
			self.poses_listWidget.setCurrentRow(0)
		#------------------------------------------------------
		# Signals
		#------------------------------------------------------
		self.pic_button.clicked.connect(self.capture)
		self.pic_sel_button.clicked.connect(self.capture_selected)
		self.add_host_pushButton.clicked.connect(self.add_host)
		self.ip_lineEdit.returnPressed.connect(self.add_host)
		self.remove_host_pushButton.clicked.connect(self.remove_host)
		self.add_pose_pushButton.clicked.connect(self.add_pose)
		self.remove_pose_pushButton.clicked.connect(self.remove_pose)
		self.sel_host.selectionChanged.connect(self.host_select_fill)

	# ------------------------------------------------------
	# Slots
	# ------------------------------------------------------
	def take_photo(self):
		print('Photo Taken!!!')
	
	def capture(self):
		time.sleep(3)
		port = int(self.port_lineEdit.text().strip())
		hosts = get_qlist_items(self.host_listWidget)
		pose_name = get_qlist_selected_items(self.poses_listWidget)[0]
		mc.send_command(hosts, port, 'PHOTO' + ' ' + str(self.get_datetime()) + '_' + pose_name)
		return

	def capture_selected(self):
		time.sleep(3)
		hosts = get_qlist_selected_items(self.host_listWidget)
		port = int(self.port_lineEdit.text().strip())
		pose_name = get_qlist_selected_items(self.poses_listWidget)[0]
		if hosts:
			mc.send_command(hosts, port, 'PHOTO' + ' ' + str(self.get_datetime()) + '_' + pose_name)

	def add_host(self):
		ip = str(self.ip_lineEdit.text().strip())
		self.host_listWidget.addItem(ip)
		sort_qlist(self.host_listWidget)
		self.export_hosts_and_port()
		#self.ip_lineEdit.clear()
		return
	
	def remove_host(self):
		selected_items = get_qlist_selected_items(self.host_listWidget)
		if selected_items:
			remove_qlist_items(selected_items, self.host_listWidget)
		self.export_hosts_and_port()
		return
		
	def export_hosts_and_port(self):
		if not os.path.exists(CAM_JSON_PATH):
			os.mkdir(CAM_JSON_PATH)
		hosts = get_qlist_items(self.host_listWidget)
		port = self.port_lineEdit.text().strip()
		cam_info = {}
		cam_info['hosts'] = hosts
		cam_info['port'] = port
		json_data.write_json(cam_info, CAM_JSON_PATH, CAM_JSON)
		return
	
	def add_pose(self):
		pose = str(self.pose_lineEdit.text().strip())
		self.poses_listWidget.addItem(pose)
		sort_qlist(self.poses_listWidget)
		self.export_pose_names()
		self.pose_lineEdit.clear()
		return
	
	def remove_pose(self):
		selected_items = get_qlist_selected_items(self.poses_listWidget)
		if selected_items:
			remove_qlist_items(selected_items, self.poses_listWidget)
			sort_qlist(self.poses_listWidget)
		self.export_pose_names()
		return
	
	def export_pose_names(self):
		if not os.path.exists(CAM_JSON_PATH):
			os.mkdir(CAM_JSON_PATH)
		pose_list = get_qlist_items(self.poses_listWidget)
		if pose_list:
			poses = {}
			poses['poses'] = {}
			for pose in pose_list:
				poses['poses'][str(pose)] = {}
			json_data.write_json(poses, CAM_JSON_PATH, FACE_POSES_JSON)
		return
	
	def shutdown_all(self):
		port = int(self.port_lineEdit.text().strip())
		hosts = get_qlist_items(self.host_listWidget)
		mc.send_command(hosts, port, 'SHUTDOWN')
		return
	
	def shutdown_one(self):
		port = int(self.port_lineEdit.text().strip())
		selected = get_qlist_selected_items(self.host_listWidget)
		hosts = list(selected)
		mc.send_command(hosts, port, 'SHUTDOWN')
		return

	def reboot_now(self, all=True):
		port = int(self.port_lineEdit.text().strip())
		hosts = []
		selected = get_qlist_selected_items(self.host_listWidget)
		hosts = list(selected)
		if all:
			hosts = get_qlist_items(self.host_listWidget)
		mc.send_command(hosts, port, 'REBOOT')
		return

	def kill_all(self):
		port = int(self.port_lineEdit.text().strip())
		hosts = get_qlist_items(self.host_listWidget)
		mc.send_command(hosts, port, 'KILL')
		return
	
	def kill_one(self):
		port = int(self.port_lineEdit.text().strip())
		selected = get_qlist_selected_items(self.host_listWidget)
		hosts = list(selected)
		mc.send_command(hosts, port, 'KILL')
		return
	
	def update_all(self):
		port = int(self.port_lineEdit.text().strip())
		hosts = get_qlist_items(self.host_listWidget)
		mc.send_command(hosts, port, 'GITPULL')
		return
	
	def update_one(self):
		port = int(self.port_lineEdit.text().strip())
		selected = get_qlist_selected_items(self.host_listWidget)
		hosts = list(selected)
		mc.send_command(hosts, port, 'GITPULL')
		return

	def host_select_fill(self):
		host = get_qlist_selected_items(self.host_listWidget)
		if host:
			self.ip_lineEdit.setText(str(host[0]))
		return

	def get_datetime(self):
		today = datetime.date.today()
		curr_time = datetime.datetime.now()
		time_list = [today.year, today.month, today.day, curr_time.hour, curr_time.minute, curr_time.second]
		letters = ['y', 'm', 'd', 'h', 'min', 's']
		time_list = list(map(lambda x: str(x), time_list))
		timestamp = ''
		for x in range(len(time_list)):
			timestamp += time_list[x]+letters[x]
		return timestamp

	def create_directory(self):
		if not os.path.exists(PHOTO_PATH):
			os.mkdir(PHOTO_PATH)
		os.mkdir(os.path.join(PHOTO_PATH, 'PHOTOS' + self.get_datetime()))
		return os.path.join(PHOTO_PATH, 'PHOTOS' + self.get_datetime())


def get_qlist_items(qwidget):
	all_items = []
	for index in range(qwidget.count()):
		all_items.append(qwidget.item(index).text())
	return all_items

def get_qlist_selected_items(qwidget):
	items = qwidget.selectedItems()
	if items:
		items = [str(x.text()) for x in items]
		return items
	return

def sort_qlist(qwidget):
	items = get_qlist_items(qwidget)
	items = sorted(items)
	qwidget.clear()
	qwidget.addItems(items)
	return items

def remove_qlist_items(items, qwidget):
	all_items = []
	for index in range(qwidget.count()):
		all_items.append(qwidget.item(index).text())
	
	all_items = list(map(lambda x: str(x), all_items))
	items = list(map(lambda x: str(x), items))

	[all_items.remove(x) for x in items if x in all_items]
	
	qwidget.clear()
	qwidget.addItems(all_items)
	return all_items

def get_hosts_and_port():
	if not os.path.exists(CAM_JSON_PATH):
		return [[], None]
	cam_info = json_data.read_json(CAM_JSON_PATH, CAM_JSON)
	hosts = sorted(cam_info['hosts'])
	port = cam_info['port']
	return [hosts, port]

def import_pose_names():
	if not os.path.exists(CAM_JSON_PATH):
		return
	poses = json_data.read_json(CAM_JSON_PATH, FACE_POSES_JSON)
	poses = sorted(poses['poses'].keys())
	return poses

def main():
	app = QtGui.QApplication(sys.argv)
	ui = MultiServerCaptureUI()
	ui.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

