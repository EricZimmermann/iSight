package com.implementai.android;

import android.content.Context;
import android.os.Bundle;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import androidx.appcompat.app.AppCompatActivity;

import android.view.LayoutInflater;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.util.ArrayList;

public class ManageTriageRequestsActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_manage_triage_requests);

        requestTriageCases("mlesko1996@gmail.com");
    }

    private void requestTriageCases(String email) {
        RequestQueue queue = Volley.newRequestQueue(this);
        JsonObjectRequest request = createJsonObjectRequest(email);
        queue.add(request);
    }

    private JsonObjectRequest createJsonObjectRequest(String email) {
        String url = String.format("http://implementai2020triage.pythonanywhere.com/get-triages?email=%s", email);

        return new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,
                (response) -> {
                    getTriageCases(response);
                },
                (error) -> { System.err.println(error.getMessage());
                });
    }

    private void getTriageCases(JSONObject response)  {
        JSONArray jsonArray = null;
        ArrayList<TriageSummary> triageSummaries = new ArrayList<>();
        try {
            System.out.println(response.getJSONArray("requests"));
            jsonArray = response.getJSONArray("requests");

            for (int i = 0; i < jsonArray.length(); i++) {

                JSONObject jsonObject = jsonArray.getJSONObject(i);
                String name = (String) jsonObject.get("name");
                String disease = (String) jsonObject.get("disease");
                String confident = (String) jsonObject.get("conf");
                double prob = (double) jsonObject.get("prob");
                byte[] imageArray = new byte[]{1,2,3};

                triageSummaries.add(new TriageSummary(name, confident, disease, prob, imageArray));
            }
//            System.out.println(triageSummaries);

//            LayoutInflater layoutInflater = (LayoutInflater) getApplicationContext()
//                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
//
//            LinearLayout parentView = (LinearLayout) layoutInflater.inflate(
//                    R.layout.activity_manage_triage_requests, null);

            TextView textView = findViewById(R.id.triage_request_summary_text);

            StringBuilder builder = new StringBuilder();

            for (TriageSummary summary: triageSummaries) {
//                LinearLayout childView = findViewById(R.id.triage_request_summary);
//
//                parentView.addView(childView);
//
//                TextView viewName = findViewById(R.id.triage_summary_name);
//                viewName.setText(summary.name);
//
//                TextView viewDescription = findViewById(R.id.triage_summary_description);
//                viewDescription.setText(summary.description);
//
//                TextView viewTimestamp = findViewById(R.id.triage_summary_timestamp);
//                viewTimestamp.setText("");
//
//                TextView viewConfidence = findViewById(R.id.triage_summary_confidence);
//                viewConfidence.setText(String.valueOf(summary.confidence));

//                parentView.addView(childView);
                builder.append(summary.name);
                builder.append("        ");
                builder.append(summary.confident);
                builder.append("            ");
                builder.append(summary.disease);
                builder.append("\n");
            }
            textView.setText(builder.toString());

        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private class TriageSummary {
        String name;
        String confident;
        String disease;
        double prob;
        double confidence;
        byte[] imageArray;

        public TriageSummary(String name, String confident, String disease, double prob,
                             byte[] imageArray) {
            this.name = name;
            this.confident = confident;
            this.disease = disease;
            this.prob = prob;
            this.imageArray = imageArray;
        }
    }
}

