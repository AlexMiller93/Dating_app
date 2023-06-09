from PIL import Image

def watermark_photo(input_image_path,
                output_image_path,
                watermark_image_path,
                position):

	base_image = Image.open(input_image_path).convert("RGBA")
	if base_image.height > 300 or base_image.width > 300:
			output_size = (300,300)
			base_image.thumbnail(output_size)
	width, height = base_image.size
	watermark = Image.open(watermark_image_path)

	if watermark.height > 300 or watermark.width > 300:
			output_size = (300,300)
			watermark.thumbnail(output_size)
			
	# add watermark to your image

	'''
	base_image.paste(watermark, position)
	base_image.show()
	base_image.save(output_image_path)
	'''

	transparent = Image.new('RGBA', (width, height), (0,0,0,0))
	transparent.paste(base_image, (0,0))
	transparent.paste(watermark, position, mask=watermark)
	transparent.show()
	transparent.save(output_image_path)

	'''
	card = Image.new("RGBA", (220, 220), (255, 255, 255))
	img = Image.open("/Users/paulvorobyev/test.png").convert("RGBA")
	x, y = img.size
	card.paste(img, (0, 0, x, y), img)
	card.save("test.png", format="png")
	'''
	if __name__ == '__main__':
		img = 'media/images/users/avatars/default.jpg'
		watermark_photo(img, 'media/images/users/avatars/default_wm.jpg',
				'media/watermark/watermark.png', position=(0,0))