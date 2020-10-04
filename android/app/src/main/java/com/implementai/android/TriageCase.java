package com.implementai.android;

class TriageCase {
    public String name;
    public String email;
    public String description;
    public byte[] imageArray;

    public TriageCase(String name, String email, String description, byte[] imageArray) {
        this.name = name;
        this.email = email;
        this.description = description;
        this.imageArray = imageArray;
    }
}
