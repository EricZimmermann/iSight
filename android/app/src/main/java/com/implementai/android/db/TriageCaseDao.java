package com.implementai.android.db;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Query;

import java.util.List;

@Dao
public interface TriageCaseDao {
    @Query("SELECT * FROM TriageCase")
    List<TriageCase> getAll();

    @Query("SELECT * FROM TriageCase WHERE uid IN (:triageCaseIds)")
    List<TriageCase> loadAllyByIds(int[] triageCaseIds);

    @Delete
    void delete(TriageCase triageCase);
}
