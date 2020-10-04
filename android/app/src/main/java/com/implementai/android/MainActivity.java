package com.implementai.android;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.view.MenuItem;
import android.view.View;
import android.widget.Toast;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.atomic.AtomicInteger;

public class MainActivity extends AppCompatActivity {

    @Override
    @RequiresApi(api = Build.VERSION_CODES.M)
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getSupportActionBar().hide();

        requestPermissions();
    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    private void requestPermissions() {
        if (this.checkSelfPermission(Manifest.permission.CAMERA)
                == PackageManager.PERMISSION_DENIED) {
            this.requestPermissions(new String[] {Manifest.permission.CAMERA},
                    RequestCodes.REQUEST_IMAGE_CAPTURE);
        }

        if (this.checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                == PackageManager.PERMISSION_DENIED) {
            this.requestPermissions(new String[] {Manifest.permission.WRITE_EXTERNAL_STORAGE},
                    RequestCodes.REQUEST_WRITE_STORAGE);
        }

        if (this.checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE)
                == PackageManager.PERMISSION_DENIED) {
            this.requestPermissions(new String[] {Manifest.permission.READ_EXTERNAL_STORAGE},
                    RequestCodes.REQUEST_READ_STORAGE);
        }

        if (this.checkSelfPermission(Manifest.permission.INTERNET)
                == PackageManager.PERMISSION_DENIED) {
            this.requestPermissions(new String[] {Manifest.permission.INTERNET},
                    RequestCodes.REQUEST_INTERNET);
        }
    }

    public void startCreateTriageRequestActivity(View view) {
        Intent intent = new Intent(this, CreateTriageRequestActivity.class);
        startActivity(intent);
    }

    public void startManageTriageRequestsActivity(View view) {
        Intent intent = new Intent(this, ManageTriageRequestsActivity.class);
        startActivity(intent);
    }
}
