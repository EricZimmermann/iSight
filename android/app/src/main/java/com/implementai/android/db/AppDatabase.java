package com.implementai.android.db;

import androidx.room.Database;
import androidx.room.RoomDatabase;

@Database(entities = {TriageCase.class}, version = 1)
public abstract class AppDatabase extends RoomDatabase {
    public abstract TriageCaseDao triageCaseDao();
}
