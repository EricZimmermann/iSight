package com.implementai.android.db;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity
public class TriageCase {
    @PrimaryKey(autoGenerate = true)
    public int uid;

    @ColumnInfo(name = "photo_filepath")
    public String photoFilepath;

    @ColumnInfo(name = "confidence")
    public float confidence;

    @ColumnInfo(name = "label")
    public String label;

}
