import urllib.request, json
baza=open("podaci.txt","w")
with urllib.request.urlopen("https://am-application.osram.info/en/getAllManufacturer/1.json") as url:
    svi_proizvodaci = json.loads(url.read().decode())
    if svi_proizvodaci["error"] == 0:
        svif=svi_proizvodaci.get("result")
        sviff=list(svif.values())
        for k in range(len(sviff)):
            marka=sviff[k]
            id_marke=marka.get("Manufacturer_id")
            ime_marke=marka.get("Manufacturer_name")
            with urllib.request.urlopen("https://am-application.osram.info/en/getAllModel/" + str(id_marke) + "/1.json") as url:
                vozila = json.loads(url.read().decode())
                if vozila["error"] == 0:
                    rjecnikvozila=vozila.get("result")
                    for i in range(len(rjecnikvozila)):
                        id_modela=rjecnikvozila[i].get("model_id")
                        ime_modela = rjecnikvozila[i].get("model_name")
                        with urllib.request.urlopen("https://am-application.osram.info/en/getAllType/"+str(id_modela)+".json") as url:
                            mod_vozila = json.loads(url.read().decode())
                            mod_vozilaf=mod_vozila.get("result")
                            for j in range(len(mod_vozilaf)):
                                mod_vozilaff=mod_vozilaf[j]
                                type_id=mod_vozilaff.get("type_id")
                                kubikaza_modela=mod_vozilaff.get("type_name")
                                snaga_modela = mod_vozilaff.get("type_kw") + "kw"
                                pocetak_proizvodnje=mod_vozilaff.get("type_from")
                                kraj_proizvodnje=mod_vozilaff.get("type_to")
                                #formatiranje_datuma_proizvodnje
                                pocetak_proizvodnje=pocetak_proizvodnje[0:4]+"."+pocetak_proizvodnje[4:6]
                                if kraj_proizvodnje != "0":
                                    kraj_proizvodnje = kraj_proizvodnje[0:4] + "." + kraj_proizvodnje[4:6]
                                with urllib.request.urlopen("https://am-application.osram.info/en/getAllUse/" + str(type_id) + ".json") as url:
                                    zarulje = json.loads(url.read().decode())
                                    svezarulje=zarulje.get("result")
                                    svezaruljef=list(svezarulje.values())
                                    for l in range(len(svezaruljef)):
                                        use_id=svezaruljef[l].get("use_id")
                                        ime_uporabe=svezaruljef[l].get("use_name")
                                        with urllib.request.urlopen("https://am-application.osram.info/en/getLampsByUse/" + str(use_id) + "/"+ str(type_id)+"/0.json") as url:
                                            zarulja = json.loads(url.read().decode())
                                            if zarulja["error"] == 0:
                                                zarulja_id = list(zarulja.get("result"))
                                                rj_zarulja = zarulja_id[0]
                                                vrsta_zarulje = rj_zarulja.get("osram_ece")
                                                print(ime_marke, ime_modela, kubikaza_modela, snaga_modela,pocetak_proizvodnje,kraj_proizvodnje,ime_uporabe, vrsta_zarulje)
                                                baza.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (ime_marke, ime_modela, kubikaza_modela, snaga_modela,pocetak_proizvodnje,kraj_proizvodnje,ime_uporabe, vrsta_zarulje))
                                            elif zarulja["error"] == 1:
                                                with urllib.request.urlopen("https://am-application.osram.info/en/getAllTechnology/" + str(use_id) + "/" + str(type_id) + ".json") as url:
                                                    tehnologija = json.loads(url.read().decode())
                                                    tehnologija_id=tehnologija.get("result")
                                                    tehnologija_idd=list(tehnologija_id.keys())
                                                    for m in range(len(tehnologija_idd)):
                                                        tehnologija_iddf=tehnologija_idd[m]
                                                        with urllib.request.urlopen("https://am-application.osram.info/en/getLampsByUse/" + str(use_id) + "/" + str(type_id) + "/"+str(tehnologija_iddf)+".json") as url:
                                                            zarulja = json.loads(url.read().decode())
                                                            zarulja_id = list(zarulja.get("result"))
                                                            rj_zarulja=zarulja_id[0]
                                                            vrsta_zarulje=rj_zarulja.get("osram_ece")
                                                            print(ime_marke,ime_modela,kubikaza_modela,snaga_modela,pocetak_proizvodnje,kraj_proizvodnje,ime_uporabe,vrsta_zarulje)
                                                            baza.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (ime_marke,ime_modela,kubikaza_modela,snaga_modela,pocetak_proizvodnje,kraj_proizvodnje,ime_uporabe,vrsta_zarulje))
print("Done")
baza.close()



