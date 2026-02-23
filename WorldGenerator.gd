extends Node2D

var yol_sahnesi = preload("res://YolParcasi.tscn")
var aktif_yollar = []
var son_yol_pozisyonu = 0
var parca_sayisi = 5

func _ready():
	for i in range(parca_sayisi):
		yol_ekle()

func _process(_delta):
	var oyuncu_y = $Player.position.y
	# Oyuncu yaklaştığında yeni yol ekle, arkadakini sil
	if oyuncu_y < son_yol_pozisyonu + 1000:
		yol_ekle()
		eski_yolu_sil()

func yol_ekle():
	var yeni_yol = yol_sahnesi.instantiate()
	yeni_yol.position.y = son_yol_pozisyonu
	add_child(yeni_yol)
	aktif_yollar.append(yeni_yol)
	son_yol_pozisyonu -= 600 # Yolun boyu kadar yukarı kaydır

func eski_yolu_sil():
	if aktif_yollar.size() > parca_sayisi + 2:
		var eski = aktif_yollar.pop_front()
		eski.queue_free()
