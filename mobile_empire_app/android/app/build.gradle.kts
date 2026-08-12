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
            // [معيار أمني مؤسسي]: إعداد مفتاح التوقيع لنسخة الإصدار
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

flutter {
    source = "../.."
}
