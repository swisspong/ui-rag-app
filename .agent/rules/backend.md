---
trigger: always_on
---

# Create Commands

ภาษา python

[text](../../backend) ระบบเป็น DDD
โดยมี contexts [text](../../backend/src/contexts)
โดยมี structure ตามนี้ [text](../../docs/backend-structure.md)
สร้าง command per file 
โดยใน command มี command, input, output file ที่อยู่ใน application layer
entities ใน domain เป็น dataclass ที่สามารถมี behavior ,value object ได้

# Create Queries
 
ภาษา python

[text](../../backend) ระบบเป็น DDD
โดยมี contexts [text](../../backend/src/contexts)
โดยมี structure ตามนี้ [text](../../docs/backend-structure.md)
สร้าง query per file
โดยใน query มี query, input ,output file ที่อยู่ใน application layer และต้องมี read-models,repositories สำหรับ read side ใน application layer 