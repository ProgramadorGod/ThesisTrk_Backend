# 📘 Relaciones entre tablas en la base de datos ThesisTrack

Este documento describe las claves foráneas y las relaciones entre las principales tablas del sistema.

## 🔗 Relaciones (Foreign Keys)

- **documents_filedocument**.`carrer_id` → **documents_carrer**.`id`  
  _(Restricción: `documents_filedocume_carrer_id_2ecb90c1_fk_documents`)_

- **documents_filedocument**.`document_type_id` → **documents_documenttype**.`id`  
  _(Restricción: `documents_filedocume_document_type_id_615e4cb8_fk_documents`)_

- **documents_filedocument**.`stage_id` → **documents_documentstage**.`id`  
  _(Restricción: `documents_filedocume_stage_id_0a74492a_fk_documents`)_

- **documents_urldocument**.`carrer_id` → **documents_carrer**.`id`  
  _(Restricción: `documents_urldocument_carrer_id_6906e1f3_fk_documents_carrer`)_

- **userz_account**.`user_type_id` → **userz_usertype**.`id`  
  _(Restricción: `userz_account_user_type_id_fkey`)_

- **userz_account_groups**.`account_id` → **userz_account**.`id`  
  _(Restricción: `userz_account_groups_account_id_fkey`)_

- **userz_account_user_permissions**.`account_id` → **userz_account**.`id`  
  _(Restricción: `userz_account_user_permissions_account_id_fkey`)_

---
_Generado automáticamente para documentación técnica._