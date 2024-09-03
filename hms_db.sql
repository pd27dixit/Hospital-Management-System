CREATE TABLE login(
    userid varchar(10) NOT NULL,
    password varchar(100) NOT NULL,
    usertype varchar(100) NOT NULL,
    PRIMARY KEY(userid)
);

CREATE TABLE patient(
    patientid varchar(10) NOT NULL,
    email text NOT NULL,
    patientname text NOT NULL,
    admissiondate timestamp NOT NULL DEFAULT current_timestamp(),
    address text NOT NULL,
    mobileno text NOT NULL,
    city text NOT NULL,
    pincode text NOT NULL,
    illness text NOT NULL,
    bloodgroup varchar(20) NOT NULL,
    gender text NOT NULL,
    age text NOT NULL,
    PRIMARY KEY(patientid)
);

CREATE TABLE doctor(
    doctorid varchar(10) NOT NULL,
    doctorname text NOT NULL,
    mobileno text NOT NULL,
    departmentname text NOT NULL,
    status text NOT NULL,
    education text NOT NULL,
    experience text NOT NULL,
    consultancy_charge text NOT NULL,
    gender text NOT NULL,
    PRIMARY KEY(doctorid)
);

CREATE TABLE appointment(
    appointmentid int(10) AUTO_INCREMENT,
    patientid varchar(10) NOT NULL,
    doctorid varchar(10) NOT NULL,
    appointmentdate date NOT NULL,
    status varchar(100) DEFAULT 'PENDING',
    PRIMARY KEY(appointmentid)
);

CREATE TABLE prescription(
    prescriptionid int(10) AUTO_INCREMENT,
    doctorid varchar(10) NOT NULL,
    patientid varchar(10) NOT NULL,
    appointmentid int(10) NOT NULL,
    treatment varchar(100) NOT NULL,
    test varchar(100),
    PRIMARY KEY(prescriptionid),
    FOREIGN KEY (patientid) REFERENCES patient(patientid),
    FOREIGN KEY (doctorid) REFERENCES doctor(doctorid),
    FOREIGN KEY (appointmentid) REFERENCES appointment(appointmentid)
);

CREATE TABLE room(
    roomno int(50) NOT NULL,
    status varchar(20) NOT NULL,
    PRIMARY KEY(roomno)
);

CREATE TABLE stay(
    stayid int(10) AUTO_INCREMENT,
    patientid varchar(10) NOT NULL,
    roomno int(10) NOT NULL,
    appointmentid int(10) NOT NULL,
    PRIMARY KEY(stayid)
);

INSERT INTO login VALUES('A1', 'admin12', 'admin');

INSERT INTO room VALUES('101', 'AVAILABLE');
INSERT INTO room VALUES('102', 'AVAILABLE');
INSERT INTO room VALUES('103', 'AVAILABLE');
INSERT INTO room VALUES('104', 'AVAILABLE');
INSERT INTO room VALUES('105', 'AVAILABLE');
INSERT INTO room VALUES('106', 'AVAILABLE');
INSERT INTO room VALUES('107', 'AVAILABLE');
INSERT INTO room VALUES('108', 'AVAILABLE');
INSERT INTO room VALUES('109', 'AVAILABLE');
INSERT INTO room VALUES('110', 'AVAILABLE');
INSERT INTO room VALUES('201', 'AVAILABLE');
INSERT INTO room VALUES('202', 'AVAILABLE');
INSERT INTO room VALUES('203', 'AVAILABLE');
INSERT INTO room VALUES('204', 'AVAILABLE');
INSERT INTO room VALUES('205', 'AVAILABLE');
INSERT INTO room VALUES('206', 'AVAILABLE');
INSERT INTO room VALUES('207', 'AVAILABLE');
INSERT INTO room VALUES('208', 'AVAILABLE');
INSERT INTO room VALUES('209', 'AVAILABLE');
INSERT INTO room VALUES('210', 'AVAILABLE');
INSERT INTO room VALUES('301', 'AVAILABLE');
INSERT INTO room VALUES('302', 'AVAILABLE');
INSERT INTO room VALUES('303', 'AVAILABLE');
INSERT INTO room VALUES('304', 'AVAILABLE');
INSERT INTO room VALUES('305', 'AVAILABLE');
INSERT INTO room VALUES('306', 'AVAILABLE');
INSERT INTO room VALUES('307', 'AVAILABLE');
INSERT INTO room VALUES('308', 'AVAILABLE');
INSERT INTO room VALUES('309', 'AVAILABLE');
INSERT INTO room VALUES('310', 'AVAILABLE');
