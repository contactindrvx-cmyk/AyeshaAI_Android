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
        if (mUploadMessage != null) {
            mUploadMessage.onReceiveValue(null);
        }
        mUploadMessage = filePathCallback;

        Intent i = new Intent(Intent.ACTION_GET_CONTENT);
        i.addCategory(Intent.CATEGORY_OPENABLE);
        i.setType("image/*"); // صرف تصویروں کے لیے تاکہ سسٹم کنفیوز نہ ہو

        try {
            // گیلری کھولنا
            PythonActivity.mActivity.startActivityForResult(Intent.createChooser(i, "Select Picture"), 100);
        } catch (Exception e) {
            mUploadMessage = null;
            return false;
        }
        return true;
    }
}
