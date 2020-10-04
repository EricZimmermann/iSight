package com.implementai.android;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;

import android.content.ContentResolver;
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
import java.io.FileNotFoundException;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class CreateTriageRequestActivity extends AppCompatActivity {


    private static final File storageDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);
    private Bitmap currentImageBitmap = null;
    private Uri imageUri;
//    private AppDatabase db = Room.databaseBuilder(getApplicationContext(),
//            AppDatabase.class, "database").build();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_triage_request);
    }

    public void startImageCaptureActivity(View view) {
        Intent imageCaptureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        if (imageCaptureIntent.resolveActivity(getPackageManager())!= null) {
            File photoFile;
            try {
                photoFile = createImageFile();
                photoFile.delete();

                imageUri = FileProvider.getUriForFile(this,
                        "com.implementai.android.provider",
                        photoFile);

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

        this.getContentResolver().notifyChange(imageUri, null);
        ContentResolver cr = this.getContentResolver();

        Bitmap imageBitmap = null;
        try {
            imageBitmap = android.provider.MediaStore.Images.Media.getBitmap(cr, imageUri);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        ImageView imageView = (ImageView) findViewById(R.id.TriageFormThumb);
        imageView.setImageBitmap(imageBitmap);
        currentImageBitmap = imageBitmap;
    }

    private File createImageFile() throws IOException {

        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        return File.createTempFile(timeStamp, ".jpg", storageDir);
    }

    public void submitRequest(View view) throws IOException, JSONException {

        TriageCase form = createCaseFromFields();

        RequestQueue queue = Volley.newRequestQueue(this);
        JsonObjectRequest request = createJsonObjectRequest(form);
        queue.add(request);
    }

    private JsonObjectRequest createJsonObjectRequest(TriageCase form) throws JSONException {
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

    private TriageCase createCaseFromFields() {
        final EditText eName = (EditText) findViewById(R.id.TriageFormName);
        String name = eName.getText().toString();

        final EditText eEmail = (EditText) findViewById(R.id.TriageFormEmail);
        String email = eEmail.getText().toString();

        final EditText eDescription = (EditText) findViewById(R.id.TriageFormDescription);
        String description = eDescription.getText().toString();

        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        currentImageBitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
        byte[] imageArray = Base64.encode(stream.toByteArray(), 0);

        return new TriageCase(name, email, description, imageArray);
    }

}
