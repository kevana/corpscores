# -*- coding: utf-8 -*-
"""SMS functions for app.

Special thanks to github.com/brendanlim/sms-fu for the carrier gateways.
"""


from flask.ext.mail import Message

from .extensions import mail


def split_msg(message):
    '''Split an sms into 160char chunks, if possible at newlines.'''
    chunks = []
    while len(message) > 160:
        # Split message into chunks gracefully at newlines
        try:
            idx = message[:160].rindex('\n')
        except ValueError:
            # No newline found in first 160 characters
            idx = 159
        chunks.append(message[:idx])
        message = message[idx:]
    if message:
        chunks.append(message)
    return chunks


def send_sms(carrier, number, message, subject=None, conn=None):
    '''Send an SMS message'''
    chunks = split_msg(message)
    for chunk in chunks:
        if subject:
            msg = Message(subject,
                          sender=mail.app.config['SMS_DEFAULT_SENDER'],
                          recipients=[str(number) + carriers[carrier]['suffix']])
        else:
            msg = Message('',
                          sender=mail.app.config['SMS_DEFAULT_SENDER'],
                          recipients=[str(number) + carriers[carrier]['suffix']])
        msg.body = chunk
        print('Sending to %s Carrier: %s' % (number, carrier))
        if conn:
            conn.send(msg)
        else:
            mail.send(msg)

# US Carriers
carriers = {
    "alltel": {
        "name": "Alltel",
        "suffix": "@message.alltel.com"
    },
    "ameritech": {
        "name": "Ameritech",
        "suffix": "@paging.acswireless.com"
    },
    "at&t": {
        "name": "AT&T",
        "suffix": "@txt.att.net"
    },
    "bell_atlantic": {
        "name": "Bell Atlantic",
        "suffix": "@message.bam.com"
    },
    "bellsouthmobility": {
        "name": "Bellsouth Mobility",
        "suffix": "@blsdcs.net"
    },
    "blueskyfrog": {
        "name": "BlueSkyFrog",
        "suffix": "@blueskyfrog.com"
    },
    "boost": {
        "name": "Boost Mobile",
        "suffix": "@myboostmobile.com"
    },
    "cellularsouth": {
        "name": "Cellular South",
        "suffix": "@csouth1.com"
    },
    "comcast": {
        "name": "Comcast PCS",
        "suffix": "@comcastpcs.textmsg.com"
    },
    "cricket": {
        "name": "Cricket",
        "suffix": "@sms.mycricket.com"
    },
    "kajeet": {
        "name": "kajeet",
        "suffix": "@mobile.kajeet.net"
    },
    "metropcs": {
        "name": "Metro PCS",
        "suffix": "@mymetropcs.com"
    },
    "nextel": {
        "name": "Nextel",
        "suffix": "@messaging.nextel.com"
    },
    "powertel": {
        "name": "Powertel",
        "suffix": "@ptel.net"
    },
    "pscwireless": {
        "name": "PSC Wireless",
        "suffix": "@sms.pscel.com"
    },
    "qwest": {
        "name": "Qwest",
        "suffix": "@qwestmp.com"
    },
    "southernlink": {
        "name": "Southern Link",
        "suffix": "@page.southernlinc.com"
    },
    "sprint": {
        "name": "Sprint PCS",
        "suffix": "@messaging.sprintpcs.com"
    },
    "suncom": {
        "name": "Suncom",
        "suffix": "@tms.suncom.com"
    },
    "t_mobile": {
        "name": "T-Mobile",
        "suffix": "@tmomail.net"
    },
    "tracfone": {
        "name": "Tracfone",
        "suffix": "@mmst5.tracfone.com"
    },
    "telus_mobility": {
        "name": "Telus Mobility",
        "suffix": "@msg.telus.com"
    },
    "uscellular": {
        "name": "US Cellular",
        "suffix": "@email.uscc.net"
    },
    "virgin": {
        "name": "Virgin Mobile",
        "suffix": "@vmobl.net"
    },
    "verizon": {
        "name": "Verizon Wireless",
        "suffix": "@vtext.com"
    }
}

# International Carriers
international_carriers = {
    "aliant_canada": {
        "name": "Aliant (Canada)",
        "suffix": "@chat.wirefree.ca"
    },
    "beeline_ua": {
        "name": "Beeline",
        "suffix": "@sms.beeline.ua"
    },
    "bellmobility_canada": {
        "name": "Bell Mobility (Canada)",
        "suffix": "@txt.bell.ca"
    },
    "bpl_mobile": {
        "name": "BPL Mobile",
        "suffix": "@bplmobile.com"
    },
    "claro_brazil": {
        "name": "Claro (Brazil)",
        "suffix": "@clarotorpedo.com.br"
    },
    "claro_nicaragua": {
        "name": "Claro (Nicaragua)",
        "suffix": "@ideasclaro-ca.com"
    },
    "du_arab_emirates": {
        "name": "Du (UAE)",
        "suffix": "@email2sms.ae"
    },
    "e_plus_germany": {
        "name": "E-Plus (Germany)",
        "suffix": "@smsmail.eplus.de"
    },
    "etisalat_arab_emirates": {
        "name": "Etisalat (UAE)",
        "suffix": "@email2sms.ae"
    },
    "fido_canada": {
        "name": "Fido",
        "suffix": "@fido.ca"
    },
    "koodoo": {
        "name": "Koodoo (Canada)",
        "suffix": "@msg.koodomobile.com"
    },
    "manitobatelecom_canada": {
        "name": "Manitoba Telecom (Canada)",
        "suffix": "@text.mtsmobility.com"
    },
    "mobinil_egypt": {
        "name": "Mobinil",
        "suffix": "@mobinil.net"
    },
    "mobistar_belgium": {
        "name": "Mobistar (Belgium)",
        "suffix": "@mobistar.be"
    },
    "mobitel": {
        "name": "Mobitel",
        "suffix": "@sms.mobitel.lk"
    },
    "movistar_spain": {
        "name": "Movistar (Spain)",
        "suffix": "@correo.movistar.net"
    },
    "northerntel_canada": {
        "name": "NorthernTel (Canada)",
        "suffix": "@txt.northerntelmobility.com"
    },
    "o2_germany": {
        "name": "o2 (Germany)",
        "suffix": "@o2online.de"
    },
    "o2_uk": {
        "name": "o2 (UK)",
        "suffix": "@mmail.co.uk"
    },
    "orange_mumbai": {
        "name": "Orange (Mumbai)",
        "suffix": "@orangemail.co.in"
    },
    "orange_netherlands": {
        "name": "Orange (Netherlands)",
        "suffix": "@sms.orange.nl"
    },
    "orange_uk": {
        "name": "Orange (UK)",
        "suffix": "@orange.net"
    },
    "rogers_wireless": {
        "name": "Rogers Wireless",
        "suffix": "@pcs.rogers.com"
    },
    "rogers_canada": {
        "name": "Rogers (Canada)",
        "suffix": "@pcs.rogers.ca"
    },
    "sasktel_canada": {
        "name": "SaskTel (canada)",
        "suffix": "@sms.sasktel.ca"
    },
    "sfr_france": {
        "name": "SFR (France)",
        "suffix": "@sfr.fr"
    },
    "t_mobile_austria": {
        "name": "T-Mobile (Austria)",
        "suffix": "@sms.t-mobile.at"
    },
    "t_mobile_germany": {
        "name": "T-Mobile (Germany)",
        "suffix": "@t-d1-sms.de"
    },
    "t_mobile_germany": {
        "name": "T-Mobile (Netherlands)",
        "suffix": "@gin.nl"
    },
    "t_mobile_uk": {
        "name": "T-Mobile (UK)",
        "suffix": "@t-mobile.uk.net"
    },
    "telebec_canada": {
        "name": "Telebec (Canada)",
        "suffix": "@txt.telebecmobilite.com"
    },
    "telefonica_spain": {
        "name": "Telefonica (Spain)",
        "suffix": "@movistar.net"
    },
    "telus_canada": {
        "name": "Telus (Canada)",
        "suffix": "@msg.telus.com"
    },
    "virgin_canada": {
        "name": "Virgin (Canada)",
        "suffix": "@vmobile.ca"
    },
    "vodafone_germany": {
        "name": "Vodafone (Germany)",
        "suffix": "@vodafone-sms.de"
    },
    "vodafone_egypt": {
        "name": "Vodafone (Egypt)",
        "suffix": "@vodafone.com.eg"
    },
    "vodafone_uk": {
        "name": "Vodafone (UK)",
        "suffix": "@sms.vodafone.net"
    },
    "vodafone_italy": {
        "name": "Vodafone (Italy)",
        "suffix": "@sms.vodafone.it"
    },
    "vodafone_jp_chuugoku": {
        "name": "Vodafone (Japan - Chuugoku)",
        "suffix": "@n.vodafone.ne.jp"
    },
    "vodafone_jp_hokkaido": {
        "name": "Vodafone (Japan - Hokkaido)",
        "suffix": "@d.vodafone.ne.jp"
    },
    "vodafone_jp_hokuriko": {
        "name": "Vodafone (Japan - Hokuriko)",
        "suffix": "@r.vodafone.ne.jp"
    },
    "vodafone_jp_kansai": {
        "name": "Vodafone (Japan - Kansai)",
        "suffix": "@k.vodafone.ne.jp"
    },
    "vodafone_jp_osaka": {
        "name": "Vodafone (Japan - Osaka)",
        "suffix": "@k.vodafone.ne.jp"
    },
    "vodafone_jp_kanto": {
        "name": "Vodafone (Japan - Kanto)",
        "suffix": "@k.vodafone.ne.jp"
    },
    "vodafone_jp_koushin": {
        "name": "Vodafone (Japan - Koushin)",
        "suffix": "@k.vodafone.ne.jp"
    },
    "vodafone_jp_tokyo": {
        "name": "Vodafone (Japan - Tokyo)",
        "suffix": "@k.vodafone.ne.jp"
    },
    "vodafone_jp_kyuushu": {
        "name": "Vodafone (Japan - Kyuushu)",
        "suffix": "@q.vodafone.ne.jp"
    },
    "vodafone_jp_okinawa": {
        "name": "Vodafone (Japan - Okinawa)",
        "suffix": "@q.vodafone.ne.jp"
    },
    "vodafone_jp_shikoku": {
        "name": "Vodafone (Japan - Shikoku)",
        "suffix": "@s.vodafone.ne.jp"
    },
    "vodafone_jp_touhoku": {
        "name": "Vodafone (Japan - Touhoku)",
        "suffix": "@h.vodafone.ne.jp"
    },
    "vodafone_jp_niigata": {
        "name": "Vodafone (Japan - Niigata)",
        "suffix": "@h.vodafone.ne.jp"
    },
    "vodafone_jp_toukai": {
        "name": "Vodafone (Japan - Toukai)",
        "suffix": "@h.vodafone.ne.jp"
    },
    "vodafone_spain": {
        "name": "Vodafone (Japan - Spain)",
        "suffix": "@vodafone.es"
    }
}

carrier_slugs = carriers.keys()
carrier_form_tuples = [(key, carriers[key]['name']) for key in carriers.keys()]
