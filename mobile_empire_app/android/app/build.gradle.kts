plugins {
    id("com.android.application")
    // يجب تطبيق ملحق Flutter Gradle بعد ملاحق Android و Kotlin
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    // تحديث مساحة الأسماء السيادية لتتوافق مع هوية المشروع
    namespace = "com.aymnguard.mobile_empire_app"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    defaultConfig {
        // [هوية إمبراطورية سيادية]: تعيين المعرف الفريد الخاص بالتطبيق
        applicationId = "com.aymnguard.mobile_empire_app"
        
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    buildTypes {
        release {
            // إيقاف مقصلة الأكواد التي تدمر ملفات الإقلاع وتسبب الانهيار
            isMinifyEnabled = false
            isShrinkResources = false
            
            // إعداد مفتاح التوقيع لنسخة الإصدار (معيار أمني مؤسسي) //
            signingConfig = signingConfigs.getByName("debug")
        }
    }
