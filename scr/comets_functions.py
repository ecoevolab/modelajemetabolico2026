import cometspy as c
import cobra.io
import pandas as pd
import os
import glob 

def comets(ruta_csv_syncoms, patron_xml, threads, cycles, mass, media, newpath):
    # 1. Guardar la ruta original 
    original_path = os.getcwd()
    
    root_path = os.path.abspath(newpath)
    os.makedirs(root_path, exist_ok=True)
    
    # --- CARGAR DATOS DE COMUNIDADES ---
    df = pd.read_csv(ruta_csv_syncoms)
    id_bacterias = df.iloc[:, 0].tolist()
    matriz_bacterias = df.iloc[:, 1:].astype(int).T.values.tolist()
    
    comunidades_finales = []
    for ensayo in matriz_bacterias:
        bacterias_presentes = [nombre for nombre, valor in zip(id_bacterias, ensayo) if valor == 1]
        comunidades_finales.append(bacterias_presentes)

    # --- CARGAR MODELOS A MEMORIA ---
    modelos_base = {}
    lista_archivos = glob.glob(patron_xml)
    
    print(f"Cargando {len(lista_archivos)} modelos SBML...")
    for path_completo in lista_archivos:
        archivo = os.path.basename(path_completo)
        model_id = archivo.split('_')[0]
        try:
            modelos_base[model_id] = cobra.io.read_sbml_model(path_completo)
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")

    # --- PARAMETROS DE SIMULACIÓN ---
    sim_params = c.params()
    sim_params.set_param('numRunThreads', threads)
    sim_params.set_param('maxCycles', cycles)
    sim_params.set_param('writeMediaLog', True)
    sim_params.set_param('MediaLogRate', 1)
    sim_params.set_param('writeTotalBiomassLog', True)
    sim_params.set_param('writeFluxLog', True)
    sim_params.set_param('FluxLogRate', 1)

    initial_mass = [0, 0, mass]

    # --- LOOP DE SIMULACIÓN ---
    for num, lista_nombres in enumerate(comunidades_finales, start=1):
        # VOLVER A LA RAÍZ de resultados para evitar anidamiento
        os.chdir(root_path)
        
        folder_name = f"comunidad_{num}"
        os.makedirs(folder_name, exist_ok=True)
        
        # ENTRAR a la carpeta de la comunidad actual
        os.chdir(folder_name)
        
        print(f"\n>>> Simulando Comunidad {num} en: {os.getcwd()}")

        try:
            test_tube = c.layout()
            
            # Cargar modelos y guardar sus nombres para las columnas del CSV
            modelos_agregados = []
            for model_id in lista_nombres:
                if model_id in modelos_base:
                    cobra_copy = modelos_base[model_id].copy()
                    processed_model = c.model(cobra_copy)
                    processed_model.initial_pop = initial_mass
                    test_tube.add_model(processed_model)
                    modelos_agregados.append(model_id) # Se guarda para el encabezado del CSV
                else:
                    print(f"Advertencia: {model_id} no encontrado en archivos XML")

            # --- CONFIGURAR MEDIO DE CULTIVO --- 
            for met, conc in media.items():
                try:
                    test_tube.set_specific_metabolite(met, conc)
                except:
                    pass

            trace_metabolites = ['ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e', 'h_e', 
                                 'k_e', 'h2o_e', 'mg2_e', 'mn2_e', 'mobd_e', 'na1_e', 'ni2_e', 
                                 'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e']

            for i in trace_metabolites:
                if i not in media:
                    try:
                        test_tube.set_specific_metabolite(i, 1000)
                    except:
                        pass
                test_tube.set_specific_static(i, 1000)

            # --- EJECUTAR COMETS ---
            experiment = c.comets(test_tube, sim_params)
            # Al haber usado os.chdir(), COMETS escribe aquí por defecto
            experiment.run(delete_files=False)
            
            # --- PROCESAR Y GUARDAR RESULTADOS ---
            final_models = experiment.total_biomass

            if final_models is not None and not final_models.empty:
                # Calcular tiempo real (ciclos * timeStep)
                time_step = experiment.parameters.all_params['timeStep']
                final_models['t'] = final_models['cycle'] * time_step
                
                # Ajustar nombres de columnas: 'cycle' + nombres bacterias + 't'
                final_models.columns = ['cycle'] + modelos_agregados + ['t']

                # Guardar CSV (ya estamos dentro de Comunidad_X)
                final_models.to_csv(f"comunidad_{num}_biomasa.csv", index=False)
                print(f"Biomasa guardada exitosamente.")
            
            # Guardar metabolitos
            df_metabolites = experiment.get_metabolite_time_series()
            if df_metabolites is not None:
                df_metabolites.to_csv(f"comunidad_{num}_metabolitos.csv", index=False)
                print(f"Metabolitos guardados exitosamente.")

            # Guardar media log
            media_log = experiment.media

            if media_log is not None and not media_log.empty:
                media_log.to_csv(f"comunidad_{num}_media.csv", index=False)
                print("Media log guardado exitosamente.")

        except Exception as e:
            print(f"Error crítico en Comunidad {num}: {e}")

    # 3. Al finalizar, volver a la carpeta donde empezamos
    os.chdir(original_path)
    print(f"\nProceso finalizado. Resultados en: {root_path}")

def media(name="lb", dil=1, vol=1):
    name = name.lower()  # Evita errores si escribes "Marine" o "LB" en mayúsculas
    res = {}

    if name == "lb":
        res = {
            "na1_e": 0.186931246 * dil * vol,
            "cl_e": 0.171820893 * dil * vol,
            "ca2_e": 8.00938E-05 * dil * vol,
            "fe2_e": 4.56128E-05 * dil * vol,
            "fe3_e": 4.56128E-05 * dil * vol,
            "so4_e": 0.000390397 * dil * vol,
            "pi_e": 0.004438244 * dil * vol,
            "mg2_e": 0.001746966 * dil * vol,
            "k_e": 0.002579814 * dil * vol,
            "ala__L_e": 0.00673446 * dil * vol,
            "asp__L_e": 0.005897688 * dil * vol,
            "asn__L_e": 0.000832583 * dil * vol,
            "glu__L_e": 0.013457487 * dil * vol,
            "gln__L_e": 0.000136849 * dil * vol,
            "gly_e": 0.004262859 * dil * vol,
            "his__L_e": 0.1643497 * dil * vol,
            "ile__L_e": 0.005336383 * dil * vol,
            "leu__L_e": 0.007280351 * dil * vol,
            "lys__L_e": 0.005814351 * dil * vol,
            "met__L_e": 0.001675513 * dil * vol,
            "phe__L_e": 0.003934815 * dil * vol,
            "pro__L_e": 0.006601119 * dil * vol,
            "ser__L_e": 0.002854614 * dil * vol,
            "thr__L_e": 0.002182673 * dil * vol,
            "trp__L_e": 0.000514129 * dil * vol,
            "tyr__L_e": 0.001048617 * dil * vol,
            "val__L_e": 0.006530201 * dil * vol,
            "arg__L_e": 0.00361645 * dil * vol,
            "cys__L_e": 0.000332928 * dil * vol,
            "cd2_e": 6.67176686E-08 * dil * vol,
            "cobalt2_e": 2.96947381E-07 * dil * vol,
            "cu_e": 5.2891188E-06 * dil * vol,
            "cu2_e": 5.2891188E-06 * dil * vol,
            "mn2_e": 1.10323638E-05 * dil * vol,
            "ni2_e": 2.07757313E-06 * dil * vol,
            "zn2_e": 0.000493722 * dil * vol,
            "ade_e": 0.000327092 * dil * vol,
            "gua_e": 0.00030603 * dil * vol,
            "csn_e": 0.000196213 * dil * vol,
            "ura_e": 0.000281475 * dil * vol,
            "nh4_e": 0.002301592 * dil * vol,
            "man_e": 0.001271121 * dil * vol,
            "pnto__R_e": 2.41749721E-06 * dil * vol,
            "btn_e": 2.75720165E-08 * dil * vol,
            "ascb__L_e": 8.51692028E-08 * dil * vol,
            "thm_e": 2.07077178E-06 * dil * vol,
            "nac_e": 1.63268622E-05 * dil * vol,
            "pydx_e": 4.43314813E-07 * dil * vol,
            "chol_e": 1.53595085E-05 * dil * vol,
            "adocbl_e": 2.58226354E-12 * dil * vol,
            "o2_e": 0.0182 * vol,
            "h2o_e": 55.50929781 * vol,
            "h_e": 1E-07 * vol
        }
    elif name == "lb+ribose":
        res = media("lb", dil)
        res["2dr5p_e"] = 0.1 * dil

    elif name == "marine":
        res = {
            "na1_e": 0.895059287633637 * dil * vol,
            "cl_e": 0.734866026900668 * dil * vol,
            "so4_e": 0.345797458779573 * dil * vol,
            "ca2_e": 0.028837264148495 * dil * vol,
            "k_e": 0.089116996725451 * dil * vol,
            "co3_e": 27.1819458806657 * dil * vol,
            "br_e": 0.067226890756303 * dil * vol,
            "f_e": 0.009587727708533 * dil * vol,
            "mg2_e": 0.066795742959209 * dil * vol,
            "fe2_e": 1.742E-05 * dil * vol,
            "fe3_e": 0.056698299480836 * dil * vol,
            "pi_e": 0.019990004997501 * dil * vol,
            "nh4_e": 0.019990004997501 * dil * vol,
            "no3_e": 0.00063108 * dil * vol,
            "ala__L_e": 0.000398 * dil * vol,
            "asp__L_e": 7.56E-05 * dil * vol,
            "asn__L_e": 0.000638 * dil * vol,
            "glu__L_e": 1.368E-05 * dil * vol,
            "gln__L_e": 0.0004 * dil * vol,
            "gly_e": 8.38E-05 * dil * vol,
            "his__L_e": 0.000228 * dil * vol,
            "ile__L_e": 0.000312 * dil * vol,
            "leu__L_e": 0.000314 * dil * vol,
            "lys__L_e": 5.36E-05 * dil * vol,
            "met__L_e": 0.0001574 * dil * vol,
            "phe__L_e": 0.0001738 * dil * vol,
            "pro__L_e": 0.0001522 * dil * vol,
            "ser__L_e": 0.0001344 * dil * vol,
            "thr__L_e": 2.44E-05 * dil * vol,
            "trp__L_e": 6.62E-05 * dil * vol,
            "val__L_e": 0.000298 * dil * vol,
            "arg__L_e": 0.0001492 * dil * vol,
            "cystin_e": 8.32E-06 * dil * vol,
            "al3_e": 1.148E-07 * dil * vol,
            "ba2_e": 9.46E-09 * dil * vol,
            "cd2_e": 1.334E-08 * dil * vol,
            "cobalt2_e": 5.94E-08 * dil * vol,
            "cr3_e": 1.186E-07 * dil * vol,
            "ga3_e": 1.29E-09 * dil * vol,
            "cu2_e": 9.9E-07 * dil * vol,
            "mn2_e": 9.6E-07 * dil * vol,
            "ni2_e": 1.09E-07 * dil * vol,
            "pb2_e": 1.678E-09 * dil * vol,
            "sr2_e": 1.256E-08 * dil * vol,
            "vanad_e": 8.58E-07 * dil * vol,
            "sn2_e": 7.58E-10 * dil * vol,
            "zn2_e": 5.66E-05 * dil * vol,
            "ti4_e": 6.26E-08 * dil * vol,
            "mobd_e": 6.14E-08 * dil * vol,
            "ade_e": 6.54E-05 * dil * vol,
            "gua_e": 6.12E-05 * dil * vol,
            "cyt_e": 3.92E-05 * dil * vol,
            "ura_e": 5.62E-05 * dil * vol,
            "nh3_e": 0.000488 * dil * vol,
            "cellb_e": 2.04E-06 * dil * vol,
            "man_e": 0.000254 * dil * vol,
            "fol_e": 5.08E-08 * dil * vol,
            "pnto__R_e": 4.84E-07 * dil * vol,
            "btn_e": 5.48E-09 * dil * vol,
            "sel_e": 1.098E-09 * dil * vol,
            "ascb__L_e": 1.704E-08 * dil * vol,
            "thm_e": 4.14E-07 * dil * vol,
            "ribflv_e": 1.062E-07 * dil * vol,
            "nac_e": 3.26E-06 * dil * vol,
            "pydxn_e": 8.86E-08 * dil * vol,
            "cbl1_e": 5.16E-13 * dil * vol,
            "o2": 0.0182 * vol,
            "h2o": 55.5092978073827 * vol,
            "h": 1E-07 * vol
        }
    elif name == "marine+ribose":
        res = media("marine", dil)
        res["2dr5p_e"] = 0.1 * dil

    elif name == "m9":
        res = {
            "glc__D_e": 0.02 * dil * vol,  
            "nh4_e": 0.0187 * dil * vol,    
            "pi_e": 0.0422 * dil * vol,     
            "so4_e": 0.0020 * dil * vol,    
            "k_e": 0.0220 * dil * vol,      
            "na1_e": 0.0840 * dil * vol,    
            "cl_e": 0.0150 * dil * vol,     
            "mg2_e": 0.0020 * dil * vol,    
            "o2_e": 0.0182 * vol ,           
            "h2o_e": 55.509 * vol ,          
            "h_e": 1E-07 * vol              
        }
        
    # 4. MEDIO MÍNIMO: M9 ACETATO
    elif name == "m9_acetate":
        res = media("m9", dil)
        if "glc__D_e" in res: 
            del res["glc__D_e"]
        res["ac_e"] = 0.04 * dil      

    # Manejo de error si el usuario pide un medio que no existe
    else:
        raise ValueError(f"Unrecognized media '{name}'. Supported: 'lb', 'lb+ribose', 'marine', 'marine+ribose', 'm9', 'm9_acetate'")

    return res

       

def load_strains(layout, models, initial_mass = 1e-8):
    for strain, gem in models.items():
        # print(f"==============Cargando modelo para {strain} desde {gem}==============")
        gem_i = cobra.io.read_sbml_model(gem)
        # print(f"=========================Modelo cargado para {strain}==============")
        gem_i = c.model(gem_i)
        gem_i.optimizer = "GLOP"
        # print(f"=========================Modelo procesado para {strain}==============")
        gem_i.id = strain
        # print(f"=========================ID establecido para {strain}==============")
        gem_i.initial_pop = [0, 0, initial_mass]
        # print(f"=========================Biomasa inicial para {strain}==============")
        layout.add_model(gem_i)
        # print(f"=========================Modelo añadido {strain}==============")

    return layout

    
def set_sim_params(args):
    # Def simulation parameters
    sim_params = c.params()
    # print(sim_params.show_params().to_string())

    # Set sim parameters
    sim_params.set_param("writeBiomassLog", True) 
    sim_params.set_param("BiomassLogName", os.path.join(args.outdir, "biomass.txt"))
    sim_params.set_param("BiomassLogRate", 1) 

    sim_params.set_param("writeFluxLog", True) 
    sim_params.set_param("FluxLogName", os.path.join(args.outdir, "flux.txt"))
    sim_params.set_param("FluxLogRate", 1)

    sim_params.set_param("writeMediaLog", True) 
    sim_params.set_param("MediaLogName", os.path.join(args.outdir, "media.txt"))
    sim_params.set_param("MediaLogRate", 1)

    sim_params.set_param("writeTotalBiomassLog", True) 
    sim_params.set_param("TotalBiomassLogName", os.path.join(args.outdir, "total_biomass.txt"))
    sim_params.set_param("totalBiomassLogRate", 1)

    sim_params.set_param("writeVelocityMultiConvLog", False) 
    sim_params.set_param("velocityMultiConvLogName", os.path.join(args.outdir, "velocity.txt"))
    sim_params.set_param("velocityMultiConvLogRate", 1)

    sim_params.set_param("numRunThreads", args.threads)
    # sim_params.set_param("randomSeed", args.seed)
    sim_params.set_param("timeStep", 0.1) # hr
    sim_params.set_param("maxCycles", args.cycles)
    sim_params.set_param("maxSpaceBiomass", 10) # gr DW
    sim_params.set_param("minSpaceBiomass", 1e-11) # gr DW
    sim_params.set_param("spaceWidth", 3.107233) # cm

    return sim_params