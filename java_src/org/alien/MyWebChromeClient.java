package org.alien;
import android.webkit.WebChromeClient;
import android.webkit.PermissionRequest;

public class MyWebChromeClient extends WebChromeClient {
    @Override
    public void onPermissionRequest(final PermissionRequest request) {
        request.grant(request.getResources());
    }
}
