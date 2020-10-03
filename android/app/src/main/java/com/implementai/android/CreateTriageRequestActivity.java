package com.implementai.android;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;

public class CreateTriageRequestActivity extends AppCompatActivity {

    private static final File storageDir = Environment.getExternalStoragePublicDirectory(
            Environment.DIRECTORY_PICTURES);
    private Bitmap currentImageBitmap = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_triage_request);
    }

    public void startImageCaptureActivity(View view) {
        Intent imageCaptureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        if (imageCaptureIntent.resolveActivity(getPackageManager())!= null) {
            File photoFile;
            Uri imageUri;
            try {
                photoFile = createImageFile();
                photoFile.delete();

                imageUri = Uri.fromFile(photoFile);
                imageCaptureIntent.putExtra(MediaStore.EXTRA_OUTPUT, imageUri);
                startActivityForResult(imageCaptureIntent, RequestCodes.REQUEST_IMAGE_CAPTURE);
            } catch (IOException e) {
                Toast.makeText(this, "IOException", Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == RequestCodes.REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            handleImageCapture(data);
        }
    }

    private static String currentPhotoPath;
    protected void handleImageCapture(Intent data) {

        Bundle extras = data.getExtras();
        assert extras != null;

        Bitmap imageBitmap = (Bitmap) extras.get("data");

        ImageView imageView = (ImageView) findViewById(R.id.TriageFormThumb);
        imageView.setImageBitmap(imageBitmap);
        currentImageBitmap = imageBitmap;
    }

    private File createImageFile() throws IOException {

        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        return File.createTempFile(timeStamp, ".jpg", storageDir);
    }

    public void submitRequest(View view) throws IOException, JSONException {

        TriageForm form = createForm();

        RequestQueue queue = Volley.newRequestQueue(this);
        JsonObjectRequest request = createJsonObjectRequest(form);
        queue.add(request);
    }

    private JsonObjectRequest createJsonObjectRequest(TriageForm form) throws JSONException {
        String url = "http://implementai2020triage.pythonanywhere.com/new-triage";

        JSONObject requestBody = new JSONObject();

        requestBody.put("name", form.name);
        requestBody.put("email", form.email);
        requestBody.put("description", form.description);
        requestBody.put("image_base64", new String(form.imageArray));

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url,
                requestBody,
                new Response.Listener<JSONObject>() {

                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println(response.toString());
                    }
                },
                new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        System.err.println(error.getMessage());
                    }
                });
        return jsonObjectRequest;
    }

    private TriageForm createForm() {
        final EditText eName = (EditText) findViewById(R.id.TriageFormName);
        String name = eName.getText().toString();

        final EditText eEmail = (EditText) findViewById(R.id.TriageFormEmail);
        String email = eEmail.getText().toString();

        final EditText eDescription = (EditText) findViewById(R.id.TriageFormDescription);
        String description = eDescription.getText().toString();

        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        currentImageBitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
        byte[] imageArray = Base64.encode(stream.toByteArray(), 0);

        return new TriageForm(name, email, description, imageArray);
    }

    private class TriageForm {
        public String name;
        public String email;
        public String description;
        public byte[] imageArray;

        public TriageForm(String name, String email, String description, byte[] imageArray) {
            this.name = name;
            this.email = email;
            this.description = description;
            this.imageArray = imageArray;
        }
    }
}
