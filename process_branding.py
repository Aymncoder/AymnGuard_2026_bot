import os
from PIL import Image, ImageDraw, ImageFont

def process_sovereign_image():
    # مسار الصورة الأصلية داخل مجلد الأصول
    input_path = "assets/717544_3.jpg"
    output_path = "assets/command_center_sovereign.png"
    
    # التأكد من وجود مجلد الأصول والصورة
    if not os.path.exists(input_path):
        print(f"التنبيه: لم يتم العثور على ملف الصورة الأساسي في المسار: {input_path}")
        return

    # فتح الصورة الأصلية
    img = Image.open(input_path)
    
    # إعداد زاوية التدوير (يمكن تعديلها عند الحاجة، مثلاً 0 للوضع الطبيعي)
    rotation_angle = 0
    rotated_img = img.rotate(rotation_angle, expand=True)
    
    # تحضير أدوات الرسم السيادي
    draw = ImageDraw.Draw(rotated_img)
    width, height = rotated_img.size
    
    # الاسم السيادي الرسمي المعتمد
    text = "AymnGuard Plus"
    
    # محاولة تحميل خط احترافي أو استخدام الافتراضي
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
    draw.text((x + shadow_offset, y + shadow_offset), text, fill=(5, 5, 5), font=font)
    
    # رسم النص الأساسي باللون الذهبي الملكي السيادي الحقيقي (#D4AF37)
    gold_sovereign_color = (212, 175, 55)
    draw.text((x, y), text, fill=gold_sovereign_color, font=font)
    
    # حفظ النتيجة النهائية بجودة فائقة داخل مجلد الأصول
    os.makedirs("assets", exist_ok=True)
    rotated_img.save(output_path, "PNG")
    print(f"تمت المعالجة وتوليد الهوية الذهبية الملكية بنجاح وحفظها في: {output_path}")

if __name__ == "__main__":
    process_sovereign_image()
