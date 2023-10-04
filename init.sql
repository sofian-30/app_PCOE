CREATE USER pcoe WITH PASSWORD 'iRMUVCCU8Z7lyyvtizJt';
ALTER ROLE pcoe WITH SUPERUSER;

CREATE TABLE monitoring (
  date TIMESTAMP DEFAULT NULL,
  table_name VARCHAR(64) DEFAULT NULL,
  integration_statut VARCHAR(8) DEFAULT NULL,
  message TEXT DEFAULT NULL,
  nb_lines INT DEFAULT NULL
);

--CREATE TABLE boond_table (
--	id_projet int8 NULL,
--	prj_etat int8 NULL,
--	prj_date text NULL,
--	prj_dateupdate text NULL,
--	prj_debut text NULL,
--	prj_fin text NULL,
--	prj_typeref int8 NULL,
--	prj_type int8 NULL,
--	prj_reference text NULL,
--	prj_devise float8 NULL,
--	prj_change float8 NULL,
--	prj_deviseagence float8 NULL,
--	prj_changeagence float8 NULL,
--	prj_adr text NULL,
--	prj_cp text NULL,
--	prj_ville text NULL,
--	prj_pays text NULL,
--	prj_lotstab float8 NULL,
--	prj_commentaires text NULL,
--	prj_turnover_excludingtax float8 NULL,
--	prj_margin_excludingtax float8 NULL,
--	prj_profitability float8 NULL,
--	id_profil_x int8 NULL,
--	id_ao float8 NULL,
--	id_crmcontact int8 NULL,
--	id_crmsociete int8 NULL,
--	id_societe_x int8 NULL,
--	id_pole_x float8 NULL,
--	id_profilcdp int8 NULL,
--	csoc_societe text NULL,
--	csoc_intervention text NULL,
--	csoc_type int8 NULL,
--	csoc_metiers text NULL,
--	csoc_web text NULL,
--	csoc_tel text NULL,
--	csoc_ville text NULL,
--	csoc_pays text NULL,
--	csoc_date text NULL,
--	id_profil_y int8 NULL,
--	id_societe_y int8 NULL,
--	id_pole_y float8 NULL,
--	id_action_previous float8 NULL,
--	id_action_next float8 NULL,
--	id_provenance int8 NULL,
--	csoc_cp text NULL,
--	id_bondecommande float8 NULL,
--	bdc_date text NULL,
--	bdc_refclient text NULL,
--	bdc_ref text NULL,
--	bdc_accordclient float8 NULL,
--	bdc_turnoverinvoicedexcludtax float8 NULL,
--	bdc_turnoverorderedexcludtax float8 NULL,
--	bdc_deltainvoicedexcludtax float8 NULL,
--	bdc_etat float8 NULL,
--	id_respuser float8 NULL,
--	bdc_typreglement text NULL,
--	bdc_condreglement float8 NULL,
--	bdc_typepayment float8 NULL,
--	id_profil int8 NULL,
--	profil_trigramme text NULL,
--	id_achat float8 NULL,
--	achat_datecrea text NULL,
--	achat_dateupdate text NULL,
--	achat_date timestamp NULL,
--	achat_etat float8 NULL,
--	achat_montantht float8 NULL,
--	achat_quantité float8 NULL,
--	achat_titre text NULL,
--	achat_ref text NULL,
--	achat_type float8 NULL,
--	achat_commentaire text NULL
--);
--
--CREATE TABLE app_table (
--    agence VARCHAR(255),
--    client VARCHAR(255),
--    num_ref_SAP VARCHAR(255),
--    code_projet_boond VARCHAR(255),
--    date_anniversaire DATE,
--    CA_maintenance_facture DECIMAL(10, 2),
--    achat_SAP DECIMAL(10, 2),
--    marge_maintenance DECIMAL(10, 2),
--    marge_pourcentage DECIMAL(5, 2),
--    montant_vente_annuel_N1 DECIMAL(10, 2),
--    montant_achat_annuel_N1 DECIMAL(10, 2),
--    mois_imputation VARCHAR(255),
--    type_support_SAP VARCHAR(255),
--    type_contrat VARCHAR(255),
--    parc_techno VARCHAR(255),
--    resp_commercial VARCHAR(255),
--    proposition_SAP_recue VARCHAR(255),
--    date_relance_client DATE,
--    proposition_seenovate_creee VARCHAR(255),
--    date_envoi_proposition DATE,
--    date_signature_proposition DATE,
--    num_commande VARCHAR(255),
--    date_creation_facture DATE,
--    commande_faite_SAP VARCHAR(255),
--    facture_SAP_recue VARCHAR(255),
--    remarques VARCHAR(2550)
--);



CREATE TABLE coefficient (
    id_coef varchar,
    annee int,
    type varchar,
    coef numeric
);

INSERT INTO coefficient (id_coef,annee,"type",coef) VALUES
	 ('SAP_BOBJ_2023',2023,'SAP_BOBJ',0.150),
	 ('SAP_BOBJ_2024',2024,'SAP_BOBJ',0.0291),
	 ('SAP_BOBJ_2025',2025,'SAP_BOBJ',0.216),
	 ('SAP_BOBJ_2026',2026,'SAP_BOBJ',0.261),
	 ('SAP_PAPER_2023',2023,'SAP_PAPER',0.285),
	 ('SAP_PAPER_2024',2024,'SAP_PAPER',0.072),
	 ('SAP_PAPER_2025',2025,'SAP_PAPER',0.293),
	 ('SAP_PAPER_2026',2026,'SAP_PAPER',0.030),
	 ('360_2023',2023,'360',0.027),
	 ('360_2024',2024,'360',0.146);
INSERT INTO coefficient (id_coef,annee,"type",coef) VALUES
	 ('360_2025',2025,'360',0.285),
	 ('360_2026',2026,'360',0.249),
	 ('N4Z_2023',2023,'N4Z',0.282),
	 ('N4Z_2024',2024,'N4Z',0.140),
	 ('N4Z_2025',2025,'N4Z',0.147),
	 ('N4Z_2026',2026,'N4Z',0.164),
	 ('marge_2023',2023,'marge',0.030),
	 ('marge_2024',2024,'marge',0.192),
	 ('marge_2025',2025,'marge',0.240),
	 ('marge_2026',2026,'marge',0.168);


CREATE TABLE app_table (
	code_projet_boond int8 NULL,
	proposition_sap_recue text NULL,
	date_relance_client text NULL,
	proposition_seenovate_creee text NULL,
	date_envoi_proposition date NULL,
	date_signature_proposition date NULL,
	num_commande text NULL,
	date_creation_facture date NULL,
	commande_faite_sap text NULL,
	facture_sap_recue text NULL,
	remarques text NULL,
	devis text NULL,
	accord_principe text NULL,
	signature_client text NULL,
	achat_editeur text NULL,
	renouvele text NULL,
	traitement_comptable text NULL,
	paiement_sap text NULL,
	demande_resiliation text NULL,
	communication_editeur text NULL,
	resilie text NULL,
	converti_extension text NULL,
	alerte_renouvellement text NULL,
	alerte_validation_devis text NULL,
	prix_achat_n1 float8 NULL,
	prix_vente_n1 float8 NULL,
	marge_n1 float8 NULL
);


CREATE TABLE boond_table (
	code_projet_boond int8 NULL,
	agence text NULL,
	client text NULL,
	num_ref_sap text NULL,
	date_anniversaire timestamp NULL,
	prix_achat_n float8 NULL,
	prix_vente_n float8 NULL,
	marge_n float8 NULL,
	type_support_sap text NULL,
	type_contrat text NULL,
	parc_techno text NULL,
	resp_commercial text NULL,
	adresse text NULL,
	ville text NULL,
	code_postal text NULL
);