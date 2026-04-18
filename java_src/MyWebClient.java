package com.raza.alien;

import android.webkit.WebChromeClient;
import android.webkit.PermissionRequest;
import android.webkit.WebView;
import android.webkit.ValueCallback;
import android.net.Uri;
import android.content.Intent;
import org.kivy.android.PythonActivity;

public class MyWebClient extends WebChromeClient {
    public static ValueCallback<Uri[]> mUploadMessage;

    @Override
    public void onPermissionRequest(final PermissionRequest request) {
        // 🔴 آواز اور مائیک کو "مین تھریڈ" پر پرمیشن دینا تاکہ اینڈرائیڈ میوٹ نہ کرے
        PythonActivity.mActivity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                request.grant(request.getResources());
            }
        });
    }

    @Override
    public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
        if (mUploadMessage != null) {
            mUploadMessage.onReceiveValue(null);
        }
        mUploadMessage = filePathCallback;
        
        // 🔴 گیلری کھولنے کا فورس (Force) کمانڈ جو ہر حال میں کام کرے گا
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("*/*"); // سب طرح کی تصویریں اور فائلیں سپورٹ کرے گا
        
        try {
            PythonActivity.mActivity.startActivityForResult(intent, 100);
        } catch (Exception e) {
            mUploadMessage = null;
            return false;
        }
        return true;
    }
}
