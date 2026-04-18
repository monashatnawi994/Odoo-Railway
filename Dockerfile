FROM odoo:16

COPY ./addons /mnt/extra-addons
COPY ./odoo.conf /etc/odoo/odoo.conf

USER root
RUN chown -R odoo:odoo /mnt/extra-addons /etc/odoo/odoo.conf
USER odoo

CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
