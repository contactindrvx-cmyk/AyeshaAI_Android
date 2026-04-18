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
        PythonActivity.mActivity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                request.grant(request.getResources());
            }
        });
    }

    // 🟢 یہ وہ فنکشن ہے جو پلس بٹن دبانے پر ہر حال میں گیلری کھولے گا
    @Override
    public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
        if (mUploadMessage != null) {
            mUploadMessage.onReceiveValue(null);
        }
        mUploadMessage = filePathCallback;

        // گیلری اور فائلز کھولنے کا اصلی اینڈرائیڈ انٹینٹ
        Intent i = new Intent(Intent.ACTION_GET_CONTENT);
        i.addCategory(Intent.CATEGORY_OPENABLE);
        i.setType("*/*"); // تصویر، آڈیو، سب کچھ سلیکٹ کرنے کے لیے

        Intent chooserIntent = Intent.createChooser(i, "Select File");
        try {
            PythonActivity.mActivity.startActivityForResult(chooserIntent, 100);
        } catch (Exception e) {
            mUploadMessage = null;
            return false;
        }
        return true;
    }
}
