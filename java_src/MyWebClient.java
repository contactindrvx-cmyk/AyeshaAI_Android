package com.raza.alien;

import android.webkit.WebChromeClient;
import android.webkit.PermissionRequest;
import android.webkit.WebView;
import android.webkit.ValueCallback;
import android.net.Uri;
import android.content.Intent;
import org.kivy.android.PythonActivity;

public class MyWebClient extends WebChromeClient {
    // تصویر اپلوڈ کا میسنجر
    public static ValueCallback<Uri[]> mUploadMessage;

    @Override
    public void onPermissionRequest(final PermissionRequest request) {
        request.grant(request.getResources());
    }

    // 🟢 یہ وہ جادو ہے جو آپ کا پلس (+) بٹن چالو کرے گا
    @Override
    public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
        if (mUploadMessage != null) {
            mUploadMessage.onReceiveValue(null);
        }
        mUploadMessage = filePathCallback;
        Intent intent = fileChooserParams.createIntent();
        try {
            // گیلری کھولنے کی ریکویسٹ (کوڈ 100)
            PythonActivity.mActivity.startActivityForResult(intent, 100);
        } catch (Exception e) {
            mUploadMessage = null;
            return false;
        }
        return true;
    }
}
