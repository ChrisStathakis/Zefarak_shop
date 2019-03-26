from django.conf import settings


MEDIA_URL = settings.MEDIA_URL
#MEDIA_URL = 'https://monastiraki.s3.amazonaws.com/media/'

CURRENCY = settings.CURRENCY
WAREHOUSE_ORDERS_TRANSCATIONS, RETAIL_TRANSCATIONS, PRODUCT_ATTRITUBE_TRANSCATION  = [settings.WAREHOUSE_ORDERS_TRANSCATIONS,
                                                                                      settings.RETAIL_TRANSCATIONS,
                                                                                      settings.PRODUCT_ATTRITUBE_TRANSCATION,
                                                                                    ]

TAXES_MODIFIER = 1.24


UNIT = (
    ('1', 'Τεμάχια'),
    ('2', 'Κιλά'),
    ('3', 'Κιβώτια')
)

PAYMENT_TYPE = (
    ('1', 'Cash'),
    ('2', 'Bank'),
    ('3', 'Credit Card'),
    ('4', 'Paypal')
    )

PAYMENT_ORDER_TYPE = (
    ('order', 'Τιμολόγιο Αποθήκης'),
    ('retailorder', 'Παραστατικά Πώλησης'),
    ('fixedcostinvoice', 'Λογαριασμοί'),
    ('payrollinvoice', 'Μισθοδοσία'),
    )

BANKS = (
    ('0', 'No Bank'),
    ('1', 'Εθνική Τράπεζα'),
    ('2', 'Τράπεζα Πειραιώς'),
    ('3', 'Interamerican'),
    )


PAYMENT_METHOD = (
    ('a', 'Αποπληρωμή Τιμολογίου'),
    ('b', 'Προκαταβολές'),
    ('c', 'Επιταγές'),
    )

TAXES_CHOICES = (("1", 13),
                ("2", 23),
                ("3", 24),
                ("4", 0)
                )

WAREHOUSE_OREDER_STATUS = (
    ('1', 'Ολοκληρώθηκε'),
    ('2', 'Δόσεις'),
    ('3', "Σε αναμονή"),
    ("4", "Ακυρώθηκε")
)

WAREHOUSE_ORDER_TYPE = (
    ('1', 'Τιμολόγιο - Δελτίο Αποστολής'),
    ('2', 'Τιμολόγιο'),
    ('3', 'Δελτίο Απόστολης'),
    ('4', 'Εισαγωγή Αποθήκης'),
    ('5', 'Εξαγωγή Αποθήκης')
)


STATUS_SITE = (
    ('1','Σε απόθεμα'),
    ('2','Inactive'),
    ('3','Διαθέσιμο με παραγγελία'),
    ('4','Προσωρινά μη διαθέσιμο'),
)


#  retail
ORDER_TYPES = [('r', 'Λιανική Πώληση'),
               ('e', 'Πώληση Eshop'),
               ('b', 'Παραστατικό Επιστροφής'),
               ('c', 'Ακυρωμένη Παραγγελία'),
               ('wa', 'Παραστατικό Εισαγωγής'),
               ('wr', 'Παραστατικό Εξαγωγής'),
               ]

ORDER_STATUS = (
    ('1', 'Νέα Παραγγελία'),
    ('2', 'Σε επεξεργασία'),
    ('3', 'Έτοιμη προς αποστολή'),
    ('4', 'Απεστάλη'),
    ('5', 'Επιστράφηκε'),
    ('6', 'Ακυρώθηκε'),
    ('7', 'Εισπράκτηκε'),
    ('8', 'Ολοκληρώθηκε') # never change that
        )


PAYROLL_CHOICES = (
    ('1', 'Μισθός'),
    ('2', 'ΙΚΑ'),
    ('3', 'ΑΣΦΑΛΙΣΤΙΚΕΣ ΕΙΣΦΟΡΕΣ'),
    ('4', 'ΗΜΕΡΟΜΗΣΘΙΟ'),
    ('5', 'ΕΡΓΟΣΗΜΟ'),
    ('6', 'ΔΩΡΟ')
    )

MEASURE_UNITS = (
    ('1', 'Τεμάχια'),
                 ('2', 'Κιλά'),
                 ('3', 'Κιβώτια')
                 )

STATUS = (('1', ''),('2', ''),('3', ''),('4', ''),)


ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)