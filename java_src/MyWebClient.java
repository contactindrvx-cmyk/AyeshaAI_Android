package com.raza.alien;

import android.webkit.WebChromeClient;
import android.webkit.PermissionRequest;
import android.webkit.WebView;
import android.webkit.ValueCallback;
import android.net.Uri;
import android.content.Intent;
import android.app.Activity;
import org.kivy.android.PythonActivity;

public class MyWebClient extends WebChromeClient {
    public static ValueCallback<Uri[]> mUploadMessage;

    @Override
    public void onPermissionRequest(final PermissionRequest request) {
        PythonActivity.mActivity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                request.grant(request.getResources());
            }
        });
    }

    @Override
    public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
        // اگر پہلے سے کوئی ریکویسٹ پھنسی ہوئی ہے، تو اسے کینسل کر کے لاک کھولیں
        if (mUploadMessage != null) {
            mUploadMessage.onReceiveValue(null);
        }
        mUploadMessage = filePathCallback;

        Intent i = new Intent(Intent.ACTION_GET_CONTENT);
        i.addCategory(Intent.CATEGORY_OPENABLE);
        i.setType("image/*");

        try {
            PythonActivity.mActivity.startActivityForResult(Intent.createChooser(i, "Select Picture"), 100);
        } catch (Exception e) {
            mUploadMessage = null;
            return false;
        }
        return true;
    }

    // 🟢 THE MASTER FIX: تصویر کو جاوا کے اندر ہی پروسیس کرنا تاکہ جام نہ ہو
    public static void handleUpload(int resultCode, Intent intent) {
        if (mUploadMessage == null) return;
        Uri[] results = null;
        try {
            if (resultCode == Activity.RESULT_OK && intent != null) {
                String dataString = intent.getDataString();
                if (dataString != null) {
                    results = new Uri[]{Uri.parse(dataString)};
                } else {
                    results = WebChromeClient.FileChooserParams.parseResult(resultCode, intent);
                }
            }
        } catch (Exception e) {
            results = null;
        }
        // یہ لائن ویب سائٹ کو تصویر دیتی ہے اور پلس بٹن کا لاک کھولتی ہے
        mUploadMessage.onReceiveValue(results);
        mUploadMessage = null;
    }
}
