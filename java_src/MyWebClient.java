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
                // یہ لائن مائیک اور آواز کے تمام فیچرز کو ان لاک کرے گی
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
        i.setType("image/*");
        i.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true); 

        try {
            PythonActivity.mActivity.startActivityForResult(Intent.createChooser(i, "Select Pictures"), 100);
        } catch (Exception e) {
            mUploadMessage = null;
            return false;
        }
        return true;
    }

    public static void handleUpload(int resultCode, Intent intent) {
        if (mUploadMessage == null) return;
        Uri[] results = null;
        try {
            if (resultCode == Activity.RESULT_OK && intent != null) {
                if (intent.getClipData() != null) {
                    int count = intent.getClipData().getItemCount();
                    results = new Uri[count];
                    for (int i = 0; i < count; i++) {
                        results[i] = intent.getClipData().getItemAt(i).getUri();
                    }
                } else if (intent.getData() != null) {
                    results = new Uri[]{intent.getData()};
                }
            }
        } catch (Exception e) {
            results = null;
        }
        mUploadMessage.onReceiveValue(results);
        mUploadMessage = null;
    }
}
