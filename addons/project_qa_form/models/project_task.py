from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class ProjectTask(models.Model):
    _inherit = "project.task"

    x_meter_attachment_ids = fields.Many2many(
        "ir.attachment",
        "project_task_meter_attachment_rel",
        "task_id",
        "attachment_id",
        string="Meter Attachments",
    )
    # x_meter_minipillar_ids = fields.One2many(
#     "ir.attachment",
#     "res_id",
#     string="MiniPillar Attachments",
#     domain=[("res_model", "=", "project.task")],
# )
    x_meter_minipillar_ids = fields.Many2many(
    "ir.attachment",
    "res_id",
    string="MiniPillar Attachments",
    domain=[("res_model", "=", "project.task")],
)
    
    x_trench_attachment_ids = fields.One2many(
    "ir.attachment",
    "res_id",
    string="Trench Attachments",
    domain=[("res_model", "=", "project.task")],
)

    # -----------------------
    # HEADER FIELDS
    # -----------------------
    x_work_order_ref = fields.Char(string="Work Order #")
    x_project_code = fields.Char(string="Project Code")

    x_project_type = fields.Selection(
        [
            ("801", "801 - Install Meter"),
            ("802", "802 - Install MiniPillar"),
            ("803", "803 - Excavation + Cable Laying"),
        ],
        string="Project Type",
    )

    x_work_region = fields.Char(string="Work Region")
    x_work_site = fields.Char(string="Work Site / Location")

    x_execution_duration_days = fields.Integer(string="Execution Duration (Days)")
    x_equipment_number = fields.Char(string="Equipment Number / رقم المعدة")
    x_project_number = fields.Char(string="Project Number / رقم المشروع")
    x_coordinates = fields.Char(string="Coordinates / الإحداثيات")
    x_branch = fields.Char(string="Branch / الفرع")
    x_non_conformity = fields.Boolean(string="Non-conformity / عدم المطابقة")
    x_remarks = fields.Text(string="Remarks / ملاحظات")

    x_supervisor_user_id = fields.Many2one(
        "res.users", string="Site Supervisor / مشرف التنفيذ"
    )
    x_consultant_partner_id = fields.Many2one(
        "res.partner", string="Consultant / الاستشاري"
    )

    # -----------------------
    # CHECKLISTS
    # -----------------------
    x_meter_check_ids = fields.One2many(
        "project.task.meter.check", "task_id", string="Meter Checklist"
    )

    x_minipillar_check_ids = fields.One2many(
        "project.task.minipillar.check", "task_id", string="MiniPillar Checklist"
    )

    x_trench_check_ids = fields.One2many(
        "project.task.trench.check", "task_id", string="Trench Checklist"
    )

    x_trench_remarks = fields.Text(string="Trench Remarks / ملاحظات الحفريات")

    # related lock flag
    x_is_locked = fields.Boolean(related="stage_id.x_locked", store=True)


    
    # -----------------------
    # ONCHANGE
    # -----------------------
    @api.onchange("x_project_type")
    def _onchange_project_type_prepare_checklists(self):
        for task in self:

            # 801 – Meter
            if task.x_project_type == "801" and not task.x_meter_check_ids:
                task.x_meter_check_ids = [
                    (0, 0, vals) for vals in task._get_meter_check_template()
                ]

            # 802 – MiniPillar
            if task.x_project_type == "802" and not task.x_minipillar_check_ids:
                # prepare both mini‑pillar checklist and trench checklist
                task.x_minipillar_check_ids = [
                    (0, 0, vals) for vals in task._get_minipillar_check_template()
                ]
                task.x_trench_check_ids = [
                    (0, 0, vals) for vals in task._get_trench_check_template()
                ]
    


            # 803 – Excavation + Cable Laying
            if task.x_project_type == "803" and not task.x_trench_check_ids:
                task.x_trench_check_ids = [
                    (0, 0, vals) for vals in task._get_trench_check_template()
                ]

    # -----------------------
    # TEMPLATES
    # -----------------------
    def _get_meter_check_template(self):
        return [
            {"sequence": 1, "description_en": "Are there any obstacles preventing installation?",
             "description_ar": "هل يوجد عائق للتركيب"},
            {"sequence": 2, "description_en": "Is the installation wall solid and suitable for mounting?",
             "description_ar": "هل جدار التركيب ثابت ومناسب للتركيب"},
            {"sequence": 3, "description_en": "Verification of electrical connections safety.",
             "description_ar": "سلامة التوصيلات الكهربائية"},
            {"sequence": 4, "description_en": "Is the meter properly aligned?",
             "description_ar": "هل العداد متوازن وغير مائل"},
            {"sequence": 5, "description_en": "Is the meter installed at an appropriate height?",
             "description_ar": "هل ارتفاع العداد مناسب"},
            {"sequence": 6, "description_en": "Is the meter number clearly indicated?",
             "description_ar": "هل رقم العداد واضح"},
            {"sequence": 7, "description_en": "Verification of CT connections.",
             "description_ar": "التأكد من توصيلات محول التيار"},
            {"sequence": 8, "description_en": "Sealing of the meter and enclosure.",
             "description_ar": "تختيم العداد والصندوق"},
            {"sequence": 9, "description_en": "Is the circuit breaker rating compliant?",
             "description_ar": "هل القاطع مطابق للمواصفات"},
            {"sequence": 10, "description_en": "Is the meter rating compliant?",
             "description_ar": "هل سعة العداد مطابقة"},
            {"sequence": 11, "description_en": "Cable protection conduits installed?",
             "description_ar": "هل مواسير حماية الكابلات مركبة"},
            {"sequence": 12, "description_en": "Meter data uploaded to system?",
             "description_ar": "هل تم ترحيل بيانات العداد للنظام"},
            {"sequence": 13, "description_en": "Any deviation from approved specs?",
             "description_ar": "هل يوجد اختلاف عن المواصفات"},
            {"sequence": 14, "description_en": "Enclosure grounded properly?",
             "description_ar": "هل تم تأريض الصندوق"},
            {"sequence": 15, "description_en": "Customer grounding connected?",
             "description_ar": "هل تأريض المشترك موصل"},
            {"sequence": 16, "description_en": "Pre-commissioning tests completed?",
             "description_ar": "هل تم تنفيذ اختبارات ما قبل التشغيل"},
        ]

    def _get_minipillar_check_template(self):
        return [
            {"sequence": 1.0, "code": "1", "ref_no": "1",
             "description_en": "Is foundation installed correctly?",
             "description_ar": "هل تم تثبيت قاعدة لوحة التوزيع بطريقة صحيحة؟"},
            {"sequence": 2.0, "code": "2", "ref_no": "2",
             "description_en": "Location of MP foundation:",
             "description_ar": "موقع قاعدة لوحة التوزيع:"},
            {"sequence": 2.1, "code": "2.1", "ref_no": "2.1",
             "description_en": "20cm away from building boundary wall?",
             "description_ar": "هل يبعد 20 سم عن حائط المبنى؟"},
            {"sequence": 2.2, "code": "2.2", "ref_no": "2.2",
             "description_en": "According to project drawing?",
             "description_ar": "حسب مخطط المشروع؟"},
            {"sequence": 3.0, "code": "3", "ref_no": "3",
             "description_en": "Is MP door and locks OK?",
             "description_ar": "هل باب لوحة التوزيع والأقفال بحالة جيدة؟"},
            {"sequence": 4.0, "code": "4", "ref_no": "4",
             "description_en": "All bolts tightened properly?",
             "description_ar": "هل جميع البراغي مثبتة بإحكام؟"},
            {"sequence": 5.0, "code": "5", "ref_no": "5",
             "description_en": "No damage to MP body or paint?",
             "description_ar": "لا يوجد تلف في جسم أو دهان اللوحة؟"},
            {"sequence": 6.0, "code": "6", "ref_no": "6",
             "description_en": "Grounding as per SEC standard?",
             "description_ar": "هل التأريض حسب مواصفات الشركة؟"},
            {"sequence": 7.0, "code": "7", "ref_no": "7",
             "description_en": "Cable termination inside MP correct?",
             "description_ar": "هل توصيل الكابل داخل اللوحة صحيح؟"},
            {"sequence": 8.0, "code": "8", "ref_no": "8",
             "description_en": "Connections checked for tightness?",
             "description_ar": "هل تم فحص شد التوصيلات؟"},
            {"sequence": 9.0, "code": "9", "ref_no": "9",
             "description_en": "Color sequence checked?",
             "description_ar": "هل تم فحص تتابع الألوان؟"},
            {"sequence": 10.0, "code": "10", "ref_no": "10",
             "description_en": "MP number and warning signs labeled?",
             "description_ar": "هل رقم اللوحة وإشارات التحذير واضحة؟"},
            {"sequence": 11.0, "code": "11", "ref_no": "11",
             "description_en": "Circuit numbers labeled?",
             "description_ar": "هل أرقام الدوائر واضحة؟"},
            {"sequence": 12.0, "code": "12", "ref_no": "12",
             "description_en": "Site cleaned and reinstated?",
             "description_ar": "هل تم تنظيف الموقع وإعادته لوضعه؟"},
        ]

    def _get_trench_check_template(self):
        return [
            {"sequence": i, "description_en": en, "statement": ar, "ref_no": str(i)}
            for i, en, ar in [
                (1, 'Is trench as per municipality map of "Right of Way"?',
                 "هل الحفريات تقع ضمن المسار المحدد حسب مخطط البلدية؟"),
                (2, "Has excavation area been properly barricaded?",
                 "هل منطقة الحفر محاطة بالحواجز اللازمة؟"),
                (3, "Is contractor signboard available?",
                 "هل توجد لوحة المقاول وتصريح الحفر؟"),
                (4, "Are traffic provisions placed?",
                 "هل وضعت معابر للسيارات والمشاة؟"),
                (5, "Are trench dimensions as per specs?",
                 "هل أبعاد الحفر حسب المواصفات؟"),
                (6, "Is excavated material removed before cable laying?",
                 "هل تمت إزالة مخلفات الحفر قبل التمديد؟"),
                (7, "Are enough manpower available?",
                 "هل يوجد عدد كافٍ من العمالة؟"),
                (8, "Any damage to existing utilities?",
                 "هل حدث ضرر للخدمات القائمة؟"),
                (9, "Is subsoil water removed?",
                 "هل تم سحب المياه من الحفرية؟"),
                (10, "Are pipes laid correctly?",
                 "هل نفذت المواسير حسب المواصفات؟"),
                (11, "Is sand placed above and below cable?",
                 "هل وضع الرمل أسفل وأعلى الكابل؟"),
                (12, "Are cable-end seals in good condition?",
                 "هل نهايات الكابل مختومة جيداً؟"),
                (13, "Are cable rollers sufficient?",
                 "هل عجلات السحب كافية ومناسبة؟"),
                (14, "Any defect noticed on cable?",
                 "هل لوحظ أي تلف بالكابل؟"),
                (15, "Are cables tied every 3 meters?",
                 "هل ربطت الكوابل كل 3 أمتار؟"),
                (16, "Is cable straight after removing rollers?",
                 "هل الكابل مستقيم بعد إزالة العجلات؟"),
                (17, "Proper spacing between cables?",
                 "هل تم ترك مسافات كافية بين الكوابل؟"),
                (18, "Clearance from other utilities?",
                 "هل يوجد خلوص كافٍ من الخدمات الأخرى؟"),
                (19, "New cable ends sealed?",
                 "هل نهايات الكابل المختومة حديثاً مغلقة؟"),
                (20, "Is warning tape laid?",
                 "هل تم وضع شريط التحذير؟"),
                (21, "Is trench backfilled?",
                 "هل تم دفان الحفرية؟"),
                (22, "Concrete done for exact drilling?",
                 "هل تم صب الخرسانة في الحفر الدقيق؟"),
                (23, "Is trench asphalted?",
                 "هل تم سفلتة الحفرية؟"),
                (24, "Asphalt restored after drilling?",
                 "هل تم إعادة الأسفلت؟"),
                (25, "Site restored to original condition?",
                 "هل أعيد الموقع إلى وضعه السابق؟"),
            ]
        ]

    # def write(self, vals):
    #     # 1) block editing if locked (except allowed groups)
    #     if vals.keys() - {"stage_id"}:
    #         for task in self:
    #             if task.x_is_locked:
    #                 if task.stage_id.name == "To Validate" and self.env.user.has_group("project_qa_form.group_qa_validator"):
    #                     continue
    #                 if task.stage_id.name == "To Approve" and self.env.user.has_group("project_qa_form.group_qa_approver"):
    #                     continue
    #                 raise AccessError(_("Task is locked in this stage."))

    #     # 2) control stage movement
    #     if "stage_id" in vals:
    #         new_stage = self.env["project.task.type"].browse(vals["stage_id"])
    #         for task in self:
    #             old = task.stage_id.name
    #             new = new_stage.name

    #             if old == "Draft" and new == "To Fill" and not self.env.user.has_group("project_qa_form.group_qa_creator"):
    #                 raise AccessError(_("Only Creator can move Draft → To Fill"))

    #             if old == "To Validate" and new == "To Approve" and not self.env.user.has_group("project_qa_form.group_qa_validator"):
    #                 raise AccessError(_("Only Validator can move To Validate → To Approve"))

    #             if old == "To Approve" and new == "Done" and not self.env.user.has_group("project_qa_form.group_qa_approver"):
    #                 raise AccessError(_("Only Approver can move To Approve → Done"))

    #     return super().write(vals)

    def write(self, vals):
        # 1) block editing if locked (except allowed groups)
        
        if vals.keys() - {"stage_id"}:
            for task in self:
                if task.x_is_locked:
                    if task.stage_id.name == "To Validate" and self.env.user.has_group("project_qa_form.group_qa_validator"):
                        continue
                    if task.stage_id.name == "To Approve" and self.env.user.has_group("project_qa_form.group_qa_approver"):
                        continue
                    raise AccessError(_("Task is locked in this stage."))

        # 2) control stage movement
        if "stage_id" in vals:
            new_stage = self.env["project.task.type"].browse(vals["stage_id"])
            stage_to_state = {
                "Draft": "01_in_progress",
                "To Fill": "01_in_progress",
                "To Validate": "04_waiting_normal",        # or "02_changes_requested" if you prefer
                "To Approve": "03_approved",               # or "04_waiting_normal" if you prefer
                "In Progress": "01_in_progress",
                "Changes Requested": "02_changes_requested",
                "Approved": "03_approved",
                "Done": "1_done",
                "Canceled": "1_canceled",
            }
            vals["state"] = stage_to_state.get(new_stage.name, "01_in_progress")

            for task in self:
                old = task.stage_id.name
                new = new_stage.name

                if old == "Draft" and new == "To Fill" and not self.env.user.has_group("project_qa_form.group_qa_creator"):
                    raise AccessError(_("Only Creator can move Draft → To Fill"))

                if old == "To Fill" and new == "To Validate" and not self.env.user.has_group("project_qa_form.group_qa_creator"):
                    raise AccessError(_("Only Creator can move To Fill → To Validate"))

                if old == "To Validate" and new == "To Approve" and not self.env.user.has_group("project_qa_form.group_qa_validator"):
                    raise AccessError(_("Only Validator can move To Validate → To Approve"))

                if old == "To Approve" and new == "Done" and not self.env.user.has_group("project_qa_form.group_qa_approver"):
                    raise AccessError(_("Only Approver can move To Approve → Done"))

        return super().write(vals)

# =========================
# CHECKLIST MODELS
# =========================
class ProjectTaskMeterCheck(models.Model):
    _name = "project.task.meter.check"
    _order = "sequence, id"

    task_id = fields.Many2one("project.task", ondelete="cascade")
    sequence = fields.Integer("S.No.")
    description_en = fields.Char("Description (EN)")
    description_ar = fields.Char("الوصف (AR)")
    answer = fields.Selection([("yes", "YES"), ("no", "NO")])


class ProjectTaskMiniPillarCheck(models.Model):
    _name = "project.task.minipillar.check"
    _order = "sequence, id"

    task_id = fields.Many2one("project.task", ondelete="cascade")
    sequence = fields.Float("Seq")
    code = fields.Char("S.No.")
    ref_no = fields.Char("الرقم")
    description_en = fields.Char("Description (EN)")
    description_ar = fields.Char("الوصف (AR)")
    answer = fields.Selection([("yes", "YES"), ("no", "NO")])


class ProjectTaskTrenchCheck(models.Model):
    _name = "project.task.trench.check"
    _order = "sequence, id"

    task_id = fields.Many2one("project.task", ondelete="cascade")
    sequence = fields.Integer("S.No.")
    description_en = fields.Char("DESCRIPTION")
    statement = fields.Char("البيان")
    ref_no = fields.Char("الرقم")
    answer = fields.Selection([("yes", "YES"), ("no", "NO")])

class ProjectTaskType(models.Model):
    _inherit = "project.task.type"
    x_locked = fields.Boolean(string="Locked Stage", default=False)



# from odoo import models, fields, api

# class ProjectTask(models.Model):
#     _inherit = "project.task"

#     x_work_order_ref = fields.Char(string="Work Order #")
#     x_project_code = fields.Char(string="Project Code")  # keep or remove from view

#     x_project_type = fields.Selection(
#         selection=[
#             ("801", "801 - Install Meter"),
#             ("802", "802 - Install MiniPillar"),
#             ("803", "803 - Excavation + Cable Laying"),
#         ],
#         string="Project Type",
#         required=False,
#     )

#     x_work_region = fields.Char(string="Work Region")
#     x_work_site = fields.Char(string="Work Site / Location")

#     x_execution_duration_days = fields.Integer(string="Execution Duration (Days)")
#     x_equipment_number = fields.Char(string="Equipment Number / رقم المعدة")
#     x_project_number = fields.Char(string="Project Number / رقم المشروع")
#     x_coordinates = fields.Char(string="Coordinates / الإحداثيات")
#     x_branch = fields.Char(string="Branch / الفرع")
#     x_non_conformity = fields.Boolean(string="Non-conformity / عدم المطابقة")
#     x_remarks = fields.Text(string="Remarks / ملاحظات")

#     x_supervisor_user_id = fields.Many2one("res.users", string="Site Supervisor / مشرف التنفيذ")
#     x_consultant_partner_id = fields.Many2one("res.partner", string="Consultant / الاستشاري")

#     # 801 checklist
#     x_meter_check_ids = fields.One2many(
#         "project.task.meter.check",
#         "task_id",
#         string="Meter Checklist",
#     )

#     # 802 checklist
#     x_minipillar_check_ids = fields.One2many(
#         "project.task.minipillar.check",
#         "task_id",
#         string="MiniPillar Checklist",
#     )

#     @api.onchange("x_project_type")
#     def _onchange_project_type_prepare_checklists(self):
#         """
#         Auto-generate checklist lines when selecting:
#         - 801 -> Meter checklist (16 rows)
#         - 802 -> MiniPillar checklist (12 rows)
#         """
#         for task in self:
#             if task.x_project_type == "801" and not task.x_meter_check_ids:
#                 task.x_meter_check_ids = [(5, 0, 0)] + [
#                     (0, 0, vals) for vals in task._get_meter_check_template()
#                 ]

#             if task.x_project_type == "802" and not task.x_minipillar_check_ids:
#                 task.x_minipillar_check_ids = [(5, 0, 0)] + [
#                     (0, 0, vals) for vals in task._get_minipillar_check_template()
#                 ]
           
#     def _get_meter_check_template(self):
#         """801 - Return the 16 rows template."""
#         return [
#             {"sequence": 1, "description_en": "Are there any obstacles preventing installation?",
#              "description_ar": "هل يوجد عائق للتركيب"},
#             {"sequence": 2, "description_en": "Is the installation wall solid and suitable for mounting?",
#              "description_ar": "هل جدار التركيب ثابت ومناسب للتركيب"},
#             {"sequence": 3, "description_en": "Verification of electrical connections safety, including the meter and enclosure.",
#              "description_ar": "سلامة التوصيلات الكهربائية وسلامة العداد وصندوق"},
#             {"sequence": 4, "description_en": "Is the meter properly aligned (not tilted) and securely fixed?",
#              "description_ar": "هل العداد متوازن وغير مائل ومحكم التثبيت"},
#             {"sequence": 5, "description_en": "Is the meter installed at an appropriate height?",
#              "description_ar": "هل ارتفاع العداد مناسب"},
#             {"sequence": 6, "description_en": "Is the meter number and power supply source clearly indicated on the meter?",
#              "description_ar": "هل يوجد رقم عداد ومصدر التغذية على العداد"},
#             {"sequence": 7, "description_en": "Verification of Current Transformer (C.T) connections.",
#              "description_ar": "التاكد من توصيلات محول التيار C.T"},
#             {"sequence": 8, "description_en": "Sealing of the meter and the enclosure.",
#              "description_ar": "تختيم العداد و الصندوق"},
#             {"sequence": 9, "description_en": "Is the circuit breaker rating compliant with the approved capacity?",
#              "description_ar": "هل سعة القاطع مطابقة لسعة المعتمدة"},
#             {"sequence": 10, "description_en": "Is the meter rating compliant with the approved capacity?",
#              "description_ar": "هل سعة الساعات مطابقة لسعة المعتمدة"},
#             {"sequence": 11, "description_en": "Have cable protection conduits been installed in accordance with the approved specifications?",
#              "description_ar": "هل تم تركيب مواسير حماية الكابلات بتفس الموصفات"},
#             {"sequence": 12, "description_en": "Uploading meter data to the system and ensuring it matches the actual installation.",
#              "description_ar": "ترحيل بيانات العدادات في النظام ومطابقتها للواقع"},
#             {"sequence": 13, "description_en": "Is there any deviation in execution from the approved technical and structural specifications?",
#              "description_ar": "وجود اختلاف في التنفيذ عن المواصفات الفنية والانشائية"},
#             {"sequence": 14, "description_en": "Has the enclosure been properly grounded in accordance with specifications?",
#              "description_ar": "هل تم تاريض الصندوق حسب المواصفات"},
#             {"sequence": 15, "description_en": "Is the customer grounding conductor connected to the neutral?",
#              "description_ar": "سلك تاريض المشترك موصل بالمحايد"},
#             {"sequence": 16, "description_en": "Have pre-commissioning tests been carried out and the test reports uploaded to the system?",
#              "description_ar": "هل تم عمل اختبارات ما قبل التشغيل وارفاق النماذج في النظام"},
#         ]

#     def _get_minipillar_check_template(self):
#         """802 - FORM-QCC-SEC-07 (12 rows)"""
#         return [
#             {"sequence": 1.0, "code": "1", "ref_no": "1",
#              "description_en": "Is foundation installed correctly?",
#              "description_ar": "هل تم تثبيت قاعدة لوحة التوزيع بطريقة صحيحة؟"},
#             {"sequence": 2.0, "code": "2", "ref_no": "2",
#              "description_en": "Location of MP foundation:",
#              "description_ar": "موقع قاعدة لوحة التوزيع:"},
#             {"sequence": 2.1, "code": "2.1", "ref_no": "2.1",
#              "description_en": "20cm away from bldg. boundary wall?",
#              "description_ar": "هل يبعد 20سم من حد حائط المبنى؟"},
#             {"sequence": 2.2, "code": "2.2", "ref_no": "2.2",
#              "description_en": "According to project drawing?",
#              "description_ar": "حسب مخطط أمر العمل؟"},
#             {"sequence": 3.0, "code": "3", "ref_no": "3",
#              "description_en": "Is MP door and locks OK?",
#              "description_ar": "هل باب لوحة التوزيع يعمل بصورة جيدة؟"},
#             {"sequence": 4.0, "code": "4", "ref_no": "4",
#              "description_en": "All four bolts are properly fixed and tightened?",
#              "description_ar": "جميع البراغي مثبتة ومربوطة بأحكام؟"},
#             {"sequence": 5.0, "code": "5", "ref_no": "5",
#              "description_en": "No damage to MP body and painting?",
#              "description_ar": "لا يوجد عطب في جسم لوحة التوزيع أو الدهان؟"},
#             {"sequence": 6.0, "code": "6", "ref_no": "6",
#              "description_en": "Grounding of MP as per SEC standard?",
#              "description_ar": "هل التأريض حسب مواصفات الشركة؟"},
#             {"sequence": 7.0, "code": "7", "ref_no": "7",
#              "description_en": "Termination of cable inside MP with proper connection?",
#              "description_ar": "هل توصيلات الكابل داخل لوحة التوزيع ربطت جيداً؟"},
#             {"sequence": 8.0, "code": "8", "ref_no": "8",
#              "description_en": "Connections checked for tightness?",
#              "description_ar": "هل تم فحص شد التوصيلات؟"},
#             {"sequence": 9.0, "code": "9", "ref_no": "9",
#              "description_en": "Color sequence inside MP checked",
#              "description_ar": "هل تم فحص تتابع الألوان داخل لوحة التوزيع ؟"},
#             {"sequence": 10.0, "code": "10", "ref_no": "10",
#              "description_en": "MP number and Monogram and danger signs is stenciled?",
#              "description_ar": "هل رقم لوحة التوزيع والشعار ولوحة الخطر مبين؟"},
#             {"sequence": 11.0, "code": "11", "ref_no": "11",
#              "description_en": "Circuit numbers are stenciled?",
#              "description_ar": "هل أرقام الدوائر مبينة؟"},
#             {"sequence": 12.0, "code": "12", "ref_no": "12",
#              "description_en": "Site cleared and reinstatement done?",
#              "description_ar": "هل الموقع نظيف والوضع معاد إلى ما كان عليه ؟"},
#         ]


# class ProjectTaskMeterCheck(models.Model):
#     _name = "project.task.meter.check"
#     _description = "Meter Checklist Line"
#     _order = "sequence, id"

#     task_id = fields.Many2one("project.task", required=True, ondelete="cascade")
#     sequence = fields.Integer(string="S.No.", required=True, default=1)
#     description_en = fields.Char(string="Description (EN)", required=True)
#     description_ar = fields.Char(string="الوصف (AR)", required=True)
#     answer = fields.Selection([("yes", "YES"), ("no", "NO")], string="Answer")


# class ProjectTaskMiniPillarCheck(models.Model):
#     _name = "project.task.minipillar.check"
#     _description = "MiniPillar Checklist Line"
#     _order = "sequence, id"

#     task_id = fields.Many2one("project.task", required=True, ondelete="cascade")
#     sequence = fields.Float(string="Seq", required=True, default=1.0)   # to sort 2.1, 2.2
#     code = fields.Char(string="S.No.", required=True)                  # shows 2.1, 2.2
#     ref_no = fields.Char(string="الرقم")
#     description_en = fields.Char(string="Description (EN)", required=True)
#     description_ar = fields.Char(string="الوصف (AR)", required=True)
#     answer = fields.Selection([("yes", "YES"), ("no", "NO")], string="Answer")

# from odoo import models, fields, api


# class ProjectTask(models.Model):
#     _inherit = "project.task"

#     # -----------------------
#     # HEADER FIELDS
#     # -----------------------
#     x_work_order_ref = fields.Char(string="Work Order #")
#     x_project_code = fields.Char(string="Project Code")

#     x_project_type = fields.Selection(
#         [
#             ("801", "801 - Install Meter"),
#             ("802", "802 - Install MiniPillar"),
#             ("803", "803 - Excavation + Cable Laying"),
#         ],
#         string="Project Type",
#     )

#     x_work_region = fields.Char(string="Work Region")
#     x_work_site = fields.Char(string="Work Site / Location")

#     x_execution_duration_days = fields.Integer(string="Execution Duration (Days)")
#     x_equipment_number = fields.Char(string="Equipment Number / رقم المعدة")
#     x_project_number = fields.Char(string="Project Number / رقم المشروع")
#     x_coordinates = fields.Char(string="Coordinates / الإحداثيات")
#     x_branch = fields.Char(string="Branch / الفرع")
#     x_non_conformity = fields.Boolean(string="Non-conformity / عدم المطابقة")
#     x_remarks = fields.Text(string="Remarks / ملاحظات")

#     x_supervisor_user_id = fields.Many2one(
#         "res.users", string="Site Supervisor / مشرف التنفيذ"
#     )
#     x_consultant_partner_id = fields.Many2one(
#         "res.partner", string="Consultant / الاستشاري"
#     )

#     # -----------------------
#     # CHECKLISTS
#     # -----------------------
#     x_meter_check_ids = fields.One2many(
#         "project.task.meter.check", "task_id", string="Meter Checklist"
#     )

#     x_minipillar_check_ids = fields.One2many(
#         "project.task.minipillar.check", "task_id", string="MiniPillar Checklist"
#     )

#     x_trench_check_ids = fields.One2many(
#         "project.task.trench.check", "task_id", string="Trench Checklist"
#     )

#     x_trench_remarks = fields.Text(string="Trench Remarks / ملاحظات الحفريات")

#     # -----------------------
#     # ONCHANGE
#     # -----------------------
#     @api.onchange("x_project_type")
#     def _onchange_project_type_prepare_checklists(self):
#         for task in self:

#             # 801 – Meter
#             if task.x_project_type == "801" and not task.x_meter_check_ids:
#                 task.x_meter_check_ids = [
#                     (0, 0, vals) for vals in task._get_meter_check_template()
#                 ]

#             # 802 – MiniPillar
#             if task.x_project_type == "802" and not task.x_minipillar_check_ids:
#                 task.x_minipillar_check_ids = [
#                     (0, 0, vals) for vals in task._get_minipillar_check_template()
#                 ]

#             # 803 – Excavation + Cable Laying
#             if task.x_project_type == "803" and not task.x_trench_check_ids:
#                 task.x_trench_check_ids = [
#                     (0, 0, vals) for vals in task._get_trench_check_template()
#                 ]

#     # -----------------------
#     # TEMPLATES
#     # -----------------------
#     def _get_meter_check_template(self):
#         return [
#             {"sequence": 1, "description_en": "Are there any obstacles preventing installation?",
#              "description_ar": "هل يوجد عائق للتركيب"},
#             {"sequence": 2, "description_en": "Is the installation wall solid and suitable for mounting?",
#              "description_ar": "هل جدار التركيب ثابت ومناسب للتركيب"},
#             {"sequence": 3, "description_en": "Verification of electrical connections safety.",
#              "description_ar": "سلامة التوصيلات الكهربائية"},
#             {"sequence": 4, "description_en": "Is the meter properly aligned?",
#              "description_ar": "هل العداد متوازن وغير مائل"},
#             {"sequence": 5, "description_en": "Is the meter installed at an appropriate height?",
#              "description_ar": "هل ارتفاع العداد مناسب"},
#             {"sequence": 6, "description_en": "Is the meter number clearly indicated?",
#              "description_ar": "هل رقم العداد واضح"},
#             {"sequence": 7, "description_en": "Verification of CT connections.",
#              "description_ar": "التأكد من توصيلات محول التيار"},
#             {"sequence": 8, "description_en": "Sealing of the meter and enclosure.",
#              "description_ar": "تختيم العداد والصندوق"},
#             {"sequence": 9, "description_en": "Is the circuit breaker rating compliant?",
#              "description_ar": "هل القاطع مطابق للمواصفات"},
#             {"sequence": 10, "description_en": "Is the meter rating compliant?",
#              "description_ar": "هل سعة العداد مطابقة"},
#             {"sequence": 11, "description_en": "Cable protection conduits installed?",
#              "description_ar": "هل مواسير حماية الكابلات مركبة"},
#             {"sequence": 12, "description_en": "Meter data uploaded to system?",
#              "description_ar": "هل تم ترحيل بيانات العداد للنظام"},
#             {"sequence": 13, "description_en": "Any deviation from approved specs?",
#              "description_ar": "هل يوجد اختلاف عن المواصفات"},
#             {"sequence": 14, "description_en": "Enclosure grounded properly?",
#              "description_ar": "هل تم تأريض الصندوق"},
#             {"sequence": 15, "description_en": "Customer grounding connected?",
#              "description_ar": "هل تأريض المشترك موصل"},
#             {"sequence": 16, "description_en": "Pre-commissioning tests completed?",
#              "description_ar": "هل تم تنفيذ اختبارات ما قبل التشغيل"},
#         ]

#     def _get_minipillar_check_template(self):
#         return [
#             {"sequence": 1.0, "code": "1", "ref_no": "1",
#              "description_en": "Is foundation installed correctly?",
#              "description_ar": "هل تم تثبيت قاعدة لوحة التوزيع بطريقة صحيحة؟"},
#             {"sequence": 2.0, "code": "2", "ref_no": "2",
#              "description_en": "Location of MP foundation:",
#              "description_ar": "موقع قاعدة لوحة التوزيع:"},
#             {"sequence": 2.1, "code": "2.1", "ref_no": "2.1",
#              "description_en": "20cm away from building boundary wall?",
#              "description_ar": "هل يبعد 20 سم عن حائط المبنى؟"},
#             {"sequence": 2.2, "code": "2.2", "ref_no": "2.2",
#              "description_en": "According to project drawing?",
#              "description_ar": "حسب مخطط المشروع؟"},
#             {"sequence": 3.0, "code": "3", "ref_no": "3",
#              "description_en": "Is MP door and locks OK?",
#              "description_ar": "هل باب لوحة التوزيع والأقفال بحالة جيدة؟"},
#             {"sequence": 4.0, "code": "4", "ref_no": "4",
#              "description_en": "All bolts tightened properly?",
#              "description_ar": "هل جميع البراغي مثبتة بإحكام؟"},
#             {"sequence": 5.0, "code": "5", "ref_no": "5",
#              "description_en": "No damage to MP body or paint?",
#              "description_ar": "لا يوجد تلف في جسم أو دهان اللوحة؟"},
#             {"sequence": 6.0, "code": "6", "ref_no": "6",
#              "description_en": "Grounding as per SEC standard?",
#              "description_ar": "هل التأريض حسب مواصفات الشركة؟"},
#             {"sequence": 7.0, "code": "7", "ref_no": "7",
#              "description_en": "Cable termination inside MP correct?",
#              "description_ar": "هل توصيل الكابل داخل اللوحة صحيح؟"},
#             {"sequence": 8.0, "code": "8", "ref_no": "8",
#              "description_en": "Connections checked for tightness?",
#              "description_ar": "هل تم فحص شد التوصيلات؟"},
#             {"sequence": 9.0, "code": "9", "ref_no": "9",
#              "description_en": "Color sequence checked?",
#              "description_ar": "هل تم فحص تتابع الألوان؟"},
#             {"sequence": 10.0, "code": "10", "ref_no": "10",
#              "description_en": "MP number and warning signs labeled?",
#              "description_ar": "هل رقم اللوحة وإشارات التحذير واضحة؟"},
#             {"sequence": 11.0, "code": "11", "ref_no": "11",
#              "description_en": "Circuit numbers labeled?",
#              "description_ar": "هل أرقام الدوائر واضحة؟"},
#             {"sequence": 12.0, "code": "12", "ref_no": "12",
#              "description_en": "Site cleaned and reinstated?",
#              "description_ar": "هل تم تنظيف الموقع وإعادته لوضعه؟"},
#         ]

#     def _get_trench_check_template(self):
#         return [
#             {"sequence": i, "description_en": en, "statement": ar, "ref_no": str(i)}
#             for i, en, ar in [
#                 (1, 'Is trench as per municipality map of "Right of Way"?',
#                  "هل الحفريات تقع ضمن المسار المحدد حسب مخطط البلدية؟"),
#                 (2, "Has excavation area been properly barricaded?",
#                  "هل منطقة الحفر محاطة بالحواجز اللازمة؟"),
#                 (3, "Is contractor signboard available?",
#                  "هل توجد لوحة المقاول وتصريح الحفر؟"),
#                 (4, "Are traffic provisions placed?",
#                  "هل وضعت معابر للسيارات والمشاة؟"),
#                 (5, "Are trench dimensions as per specs?",
#                  "هل أبعاد الحفر حسب المواصفات؟"),
#                 (6, "Is excavated material removed before cable laying?",
#                  "هل تمت إزالة مخلفات الحفر قبل التمديد؟"),
#                 (7, "Are enough manpower available?",
#                  "هل يوجد عدد كافٍ من العمالة؟"),
#                 (8, "Any damage to existing utilities?",
#                  "هل حدث ضرر للخدمات القائمة؟"),
#                 (9, "Is subsoil water removed?",
#                  "هل تم سحب المياه من الحفرية؟"),
#                 (10, "Are pipes laid correctly?",
#                  "هل نفذت المواسير حسب المواصفات؟"),
#                 (11, "Is sand placed above and below cable?",
#                  "هل وضع الرمل أسفل وأعلى الكابل؟"),
#                 (12, "Are cable-end seals in good condition?",
#                  "هل نهايات الكابل مختومة جيداً؟"),
#                 (13, "Are cable rollers sufficient?",
#                  "هل عجلات السحب كافية ومناسبة؟"),
#                 (14, "Any defect noticed on cable?",
#                  "هل لوحظ أي تلف بالكابل؟"),
#                 (15, "Are cables tied every 3 meters?",
#                  "هل ربطت الكوابل كل 3 أمتار؟"),
#                 (16, "Is cable straight after removing rollers?",
#                  "هل الكابل مستقيم بعد إزالة العجلات؟"),
#                 (17, "Proper spacing between cables?",
#                  "هل تم ترك مسافات كافية بين الكوابل؟"),
#                 (18, "Clearance from other utilities?",
#                  "هل يوجد خلوص كافٍ من الخدمات الأخرى؟"),
#                 (19, "New cable ends sealed?",
#                  "هل نهايات الكابل المختومة حديثاً مغلقة؟"),
#                 (20, "Is warning tape laid?",
#                  "هل تم وضع شريط التحذير؟"),
#                 (21, "Is trench backfilled?",
#                  "هل تم دفان الحفرية؟"),
#                 (22, "Concrete done for exact drilling?",
#                  "هل تم صب الخرسانة في الحفر الدقيق؟"),
#                 (23, "Is trench asphalted?",
#                  "هل تم سفلتة الحفرية؟"),
#                 (24, "Asphalt restored after drilling?",
#                  "هل تم إعادة الأسفلت؟"),
#                 (25, "Site restored to original condition?",
#                  "هل أعيد الموقع إلى وضعه السابق؟"),
#             ]
#         ]


# # =========================
# # CHECKLIST MODELS
# # =========================
# class ProjectTaskMeterCheck(models.Model):
#     _name = "project.task.meter.check"
#     _order = "sequence, id"

#     task_id = fields.Many2one("project.task", ondelete="cascade")
#     sequence = fields.Integer("S.No.")
#     description_en = fields.Char("Description (EN)")
#     description_ar = fields.Char("الوصف (AR)")
#     answer = fields.Selection([("yes", "YES"), ("no", "NO")])


# class ProjectTaskMiniPillarCheck(models.Model):
#     _name = "project.task.minipillar.check"
#     _order = "sequence, id"

#     task_id = fields.Many2one("project.task", ondelete="cascade")
#     sequence = fields.Float("Seq")
#     code = fields.Char("S.No.")
#     ref_no = fields.Char("الرقم")
#     description_en = fields.Char("Description (EN)")
#     description_ar = fields.Char("الوصف (AR)")
#     answer = fields.Selection([("yes", "YES"), ("no", "NO")])


# class ProjectTaskTrenchCheck(models.Model):
#     _name = "project.task.trench.check"
#     _order = "sequence, id"

#     task_id = fields.Many2one("project.task", ondelete="cascade")
#     sequence = fields.Integer("S.No.")
#     description_en = fields.Char("DESCRIPTION")
#     statement = fields.Char("البيان")
#     ref_no = fields.Char("الرقم")
#     answer = fields.Selection([("yes", "YES"), ("no", "NO")])

