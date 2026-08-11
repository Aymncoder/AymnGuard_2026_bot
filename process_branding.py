import os
from PIL import Image, ImageDraw, ImageFont

def process_sovereign_image():
    
        # مسار الصورة الأصلية الفعلية بعد الرفع
    input_path = "retouch_1786491084607.JPEG" 
    output_path = "assets/command_center_sovereign.png"

    # التأكد من وجود مجلد الأصول والصورة
    if not os.path.exists(input_path):
        print(f"خطأ: الملف غير موجود في المسار {input_path}")
        return

    # فتح الصورة الأصلية
    img = Image.open(input_path)
    
    # إعداد زاوية التدوير مع فلتر LANCZOS لضمان دقة وتجنب التعرجات البكسلية
    rotation_angle = 0
    rotated_img = img.rotate(rotation_angle, expand=True, resample=Image.Resampling.LANCZOS)
    
    # تحضير أدوات الرسم السيادي
    draw = ImageDraw.Draw(rotated_img)
    width, height = rotated_img.size
    
    # الاسم السيادي الرسمي المعتمد
    text = "AymnGuard Plus"
    
    # محاولة تحميل خط احترافي أو استخدام الافتراضي بنسب ديناميكية
    try:
        font = ImageFont.truetype("arial.ttf", size=int(width * 0.052))
    except IOError:
        font = ImageFont.load_default()
        
    # حساب أبعاد النص لتوسيطه بدقة مذهلة في المكان الأكثر جاذبية
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) / 2
    y = height - int(height * 0.14)  # وضع الاسم في الثلث السفلي لإعطاء طابع سينمائي فاخر
    
    # رسم طبقة ظل سوداء خفية لإعطاء عمق ثلاثي الأبعاد للنص
    shadow_offset = 3
    draw.text((x + shadow_offset, y + shadow_offset), text, fill=(10, 10, 10), font=font)
    
    # رسم النص الأساسي باللون الذهبي الملكي السيادي الحقيقي (#D4AF37)
    gold_sovereign_color = (212, 175, 55)
    draw.text((x, y), text, fill=gold_sovereign_color, font=font)
    
    # حفظ النتيجة النهائية بجودة فائقة داخل مجلد الأصول مع تحسين الحجم
    os.makedirs("assets", exist_ok=True)
    rotated_img.save(output_path, "PNG", optimize=True)
    print(f"تمت المعالجة وتوليد الهوية الذهبية الملكية بنجاح بمعايير الجودة الفائقة: {output_path}")

if __name__ == "__main__":
    process_sovereign_image()
