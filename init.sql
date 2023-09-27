CREATE USER pcoe WITH PASSWORD 'iRMUVCCU8Z7lyyvtizJt';
ALTER ROLE pcoe WITH SUPERUSER;

CREATE TABLE monitoring (
  date TIMESTAMP DEFAULT NULL,
  table_name VARCHAR(64) DEFAULT NULL,
  integration_statut VARCHAR(8) DEFAULT NULL,
  message TEXT DEFAULT NULL,
  nb_lines INT DEFAULT NULL
);

CREATE TABLE boond_table (
	id_projet int8 NULL,
	prj_etat int8 NULL,
	prj_date text NULL,
	prj_dateupdate text NULL,
	prj_debut text NULL,
	prj_fin text NULL,
	prj_typeref int8 NULL,
	prj_type int8 NULL,
	prj_reference text NULL,
	prj_devise float8 NULL,
	prj_change float8 NULL,
	prj_deviseagence float8 NULL,
	prj_changeagence float8 NULL,
	prj_adr text NULL,
	prj_cp text NULL,
	prj_ville text NULL,
	prj_pays text NULL,
	prj_lotstab float8 NULL,
	prj_commentaires text NULL,
	prj_turnover_excludingtax float8 NULL,
	prj_margin_excludingtax float8 NULL,
	prj_profitability float8 NULL,
	id_profil_x int8 NULL,
	id_ao float8 NULL,
	id_crmcontact int8 NULL,
	id_crmsociete int8 NULL,
	id_societe_x int8 NULL,
	id_pole_x float8 NULL,
	id_profilcdp int8 NULL,
	csoc_societe text NULL,
	csoc_intervention text NULL,
	csoc_type int8 NULL,
	csoc_metiers text NULL,
	csoc_web text NULL,
	csoc_tel text NULL,
	csoc_ville text NULL,
	csoc_pays text NULL,
	csoc_date text NULL,
	id_profil_y int8 NULL,
	id_societe_y int8 NULL,
	id_pole_y float8 NULL,
	id_action_previous float8 NULL,
	id_action_next float8 NULL,
	id_provenance int8 NULL,
	csoc_cp text NULL,
	id_bondecommande float8 NULL,
	bdc_date text NULL,
	bdc_refclient text NULL,
	bdc_ref text NULL,
	bdc_accordclient float8 NULL,
	bdc_turnoverinvoicedexcludtax float8 NULL,
	bdc_turnoverorderedexcludtax float8 NULL,
	bdc_deltainvoicedexcludtax float8 NULL,
	bdc_etat float8 NULL,
	id_respuser float8 NULL,
	bdc_typreglement text NULL,
	bdc_condreglement float8 NULL,
	bdc_typepayment float8 NULL,
	id_profil int8 NULL,
	profil_trigramme text NULL,
	id_achat float8 NULL,
	achat_datecrea text NULL,
	achat_dateupdate text NULL,
	achat_date timestamp NULL,
	achat_etat float8 NULL,
	achat_montantht float8 NULL,
	achat_quantité float8 NULL,
	achat_titre text NULL,
	achat_ref text NULL,
	achat_type float8 NULL,
	achat_commentaire text NULL
);

CREATE TABLE app_table (
    agence VARCHAR(255),
    client VARCHAR(255),
    num_ref_SAP VARCHAR(255),
    code_projet_boond VARCHAR(255),
    date_anniversaire DATE,
    CA_maintenance_facture DECIMAL(10, 2),
    achat_SAP DECIMAL(10, 2),
    marge_maintenance DECIMAL(10, 2),
    marge_pourcentage DECIMAL(5, 2),
    montant_vente_annuel_N1 DECIMAL(10, 2),
    montant_achat_annuel_N1 DECIMAL(10, 2),
    mois_imputation VARCHAR(255),
    type_support_SAP VARCHAR(255),
    type_contrat VARCHAR(255),
    parc_techno VARCHAR(255),
    resp_commercial VARCHAR(255),
    proposition_SAP_recue VARCHAR(255),
    date_relance_client DATE,
    proposition_seenovate_creee VARCHAR(255),
    date_envoi_proposition DATE,
    date_signature_proposition DATE,
    num_commande VARCHAR(255),
    date_creation_facture DATE,
    commande_faite_SAP VARCHAR(255),
    facture_SAP_recue VARCHAR(255),
    remarques VARCHAR(2550)
);