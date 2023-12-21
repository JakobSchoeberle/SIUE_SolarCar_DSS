extern crate adafruit_gps;
extern crate cantact;


use adafruit_gps::{Gps, GpsSentence};
use adafruit_gps::NmeaOutput;
use cantact::{Interface, Frame};

fn print_frame(f: Frame) {
    let ts = match f.timestamp {
        Some(t) => format!("{:.6}\t", t.as_secs_f32()),
        None => String::new(),
    };

    if f.err {
        println!("{}  ch:{} error frame", ts, f.channel);
    }

    let mut s = format!("{}  ch:{} {:03X}", ts, f.channel, f.can_id,);

    s = if f.fd {
        format!("{}   [{:02}]  ", s, f.data_len())
    } else {
        format!("{}   [{:01}]  ", s, f.data_len())
    };

    for b in f.data.iter().take(f.data_len()) {
        s = format!("{}{:02X} ", s, b);
    }
    println!("{}", s)
}

fn gpsupdate(gps2: &mut Gps) {
    let values = gps2.update();
        match values {
            GpsSentence::InvalidSentence => println!("Invalid sentence, try again"),
            GpsSentence::InvalidBytes => println!("Invalid bytes given, try again"),
            GpsSentence::NoConnection => println!("No connection with gps"),
            GpsSentence::GGA(sentence) => {
                println!("UTC: {}\nLat:{}, Long:{}, Sats:{}, MSL Alt:{}",
                sentence.utc, sentence.lat.unwrap_or(0.0), sentence.long.unwrap_or(0.0), sentence.satellites_used,
                sentence.msl_alt.unwrap_or(0.0));
            }
            GpsSentence::GSA(sentence) => {
                println!("PDOP:{}, VDOP:{}, HDOP:{}",
                sentence.pdop.unwrap_or(0.0), sentence.vdop.unwrap_or(0.0), sentence.hdop.unwrap_or(0.0))
            }
            _ => {
                ()
            }
        }
}

fn main() {

    // Open the port that is connected to the GPS module.
    let mut gps = Gps::new("/dev/serial0", "9600");
    // Give settings here.
    gps.pmtk_314_api_set_nmea_output(NmeaOutput{gga: 1, gsa: 1, gsv: 1,  gll: 1, rmc: 1, vtg: 1, pmtkchn_interval: 1 });
    let r = gps.pmtk_220_set_nmea_updaterate("1000");
    println!("{:?}", r);

    // Open a connection to the Cantact device
    let mut cantact_interface = Interface::new()
    .expect("failed to start interface");
    // Start reciving data from the Cantact device
    cantact_interface.start(move |f: Frame| {
        print_frame(f);
    })
    .expect("failed to start start");

    loop {
        gpsupdate(&mut gps);
        std::thread::sleep(std::time::Duration::from_millis(100));
    }

}