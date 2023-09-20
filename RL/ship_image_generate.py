from PIL import Image, ImageDraw

# 이미지 크기 설정
img_size = (200, 200)

# 이미지 객체 생성 (배경 투명)
img = Image.new('RGBA', img_size, color=(0, 0, 0, 0))

# 그리기 객체 생성
draw = ImageDraw.Draw(img)

# 원 그리기
draw.ellipse((50, 50, 100, 100), fill='blue')

# 이미지 저장
img.save('bullet.png')
