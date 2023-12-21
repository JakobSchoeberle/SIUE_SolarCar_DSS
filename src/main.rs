extern crate adafruit_gps;
extern crate cantact;

use adafruit_gps::{Gps, GpsSentence};
use adafruit_gps::NmeaOutput;

fn main() {

    // Open the port that is connected to the GPS module.
    let mut gps = Gps::new("/dev/serial0", "9600");
    // Give settings here.
    gps.pmtk_314_api_set_nmea_output(NmeaOutput{gga: 1, gsa: 1, gsv: 1,  gll: 1, rmc: 1, vtg: 1, pmtkchn_interval: 1 });
    let r = gps.pmtk_220_set_nmea_updaterate("1000");
    println!("{:?}", r);

    /*
    let can = cantact::Interface::new();
    let mut interface = can.unwrap();
    let output = cantact::Interface::set_monitor(&mut interface, 1, true);
    let message = output.unwrap();
    */

    fn gpsupdate(|gps2: &mut gps|) {
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

    loop {
        gpsupdate(&mut gps)
    }

}