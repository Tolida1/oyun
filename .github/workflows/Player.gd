extends CharacterBody2D

var hiz = 400
var ileri_hiz = -200 # Sürekli yukarı gider

func _physics_process(_delta):
	velocity.y = ileri_hiz
	
	# Dokunmatik kontrol (Ekranın sağına/soluna basma)
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		var dokunma_x = get_global_mouse_position().x
		if dokunma_x > get_viewport_rect().size.x / 2:
			velocity.x = hiz # Sağa git
		else:
			velocity.x = -hiz # Sola git
	else:
		velocity.x = 0
		
	move_and_slide()
