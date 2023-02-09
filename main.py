import tkinter as tk
from tkinter import ttk

def main():
	# create the main window
	root = tk.Tk()
	root.title("stats calculator")
	root.geometry("1600x900")
	root.columnconfigure(0, weight=1)
	root.resizable(False, False)
	# atk
	atk_frame = tk.Frame(root)
	atk_frame.grid(row = 0, pady=(20,5), padx=(80,5), columnspan=2, sticky='w')
	atk = Atk(atk_frame, 70)
	# e_atk
	e_atk_frame = tk.Frame(root)
	e_atk_frame.grid(row= 2, pady=(5, 10), padx=(80,0), columnspan=2, sticky='w')
	e_atk = ElementAtk(e_atk_frame, 17)
	# crit
	crit_frame = tk.Frame(root)
	crit_frame.grid(row=4, pady=20, padx=(80,0), columnspan=2, sticky='w')
	crit = Crit(crit_frame, 10, 10)
	# skill
	skill_frame = tk.Frame(root)
	skill_frame.grid(row=8, pady=(10, 0), padx=(80,0), columnspan=2, sticky='w')
	skill = SkillBasicEle(skill_frame, 0, 'skill %')
	# basic
	basic_frame = tk.Frame(root)
	basic_frame.grid(row=9, padx=(80, 0), columnspan=2, sticky='w')
	basic = SkillBasicEle(basic_frame, 0, 'basic ATK %')
	# ele DMG %
	e_DMG_per_frame = tk.Frame(root)
	e_DMG_per_frame.grid(row=10, pady=(0, 10), padx=(80, 0), columnspan=2, sticky='w')
	basic = SkillBasicEle(e_DMG_per_frame, 0, 'Ele DMG %')
	# di
	ep_frame = tk.Frame(root)
	ep_frame.grid(row=11, pady=20, padx=(80, 0), columnspan=2, sticky='w')
	di = DefIgn(ep_frame, 100)
	# ep
	ep_frame = tk.Frame(root)
	ep_frame.grid(row=12, pady=20, padx=(80, 0), columnspan=2, sticky='w')
	di = Ep(ep_frame, 100)



	root.mainloop()

class Atk:
	def __init__(self, root, stat_increase: int, stats_row: int = 0) -> None:
		self.stat_increase = stat_increase
		self.root = root
		self.stats_row = stats_row

		# row 1
		# base atk
		self.base_atk = tk.Label(self.root, text=f"base ATK:", anchor='w', width=15)
		self.base_atk.grid(row=self.stats_row, column=0)

		self.base_atk_entry = tk.Entry(self.root)
		self.base_atk_entry.insert(1000, '1000')
		self.base_atk_entry.grid(row=self.stats_row, column=1, padx= (0, 120))

		# increase
		self.label = tk.Label(self.root, text=f"+ ATK:", anchor='w', width=20)
		self.label.grid(row=self.stats_row, column=2)

		self.stat_increase_entry = tk.Entry(self.root)
		self.stat_increase_entry.insert(stat_increase, str(stat_increase))
		self.stat_increase_entry.grid(row=self.stats_row, column=3, sticky='w')

		#progress_mod
		self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress.grid(row=self.stats_row , column=4, padx= (200,20))

		# row 2
		# bonus atk %
		self.bonus_atk_percent = tk.Label(self.root, text= 'ATK bonus %:', anchor='w', width=15)
		self.bonus_atk_percent.grid(row=self.stats_row + 1, column = 0)

		self.bonus_atk_percent_entry = tk.Entry(self.root)
		self.bonus_atk_percent_entry.insert(0, "0")
		self.bonus_atk_percent_entry.grid(row=self.stats_row + 1, column=1, padx=(0, 120))

		# bonus atk
		self.bonus_atk = tk.Label(self.root, text='ATK bonus:', anchor='w', width=20)
		self.bonus_atk.grid(row=self.stats_row + 1, column=2)

		self.bonus_atk_entry = tk.Entry(self.root)
		self.bonus_atk_entry.insert(0, "0")
		self.bonus_atk_entry.grid(row=self.stats_row + 1, column=3, sticky='w')

		self.base_atk_entry.bind("<Return>", lambda e: self.set_progress())
		self.bonus_atk_percent_entry.bind("<Return>", lambda e : self.set_progress())
		self.bonus_atk_entry.bind("<Return>", lambda e : self.set_progress())
		self.stat_increase_entry.bind("<Return>", lambda e : self.set_progress())

	def calc_DPS_increase(self, increase: float = 0) -> float:
		# get value
		base = float(self.base_atk_entry.get())
		bonus = float(self.bonus_atk_entry.get())
		bonus_perc = float(self.bonus_atk_percent_entry.get()) / 100
		# calculate increase
		DPS_multiplier = (1 + (base + increase * (1 + bonus_perc / 100) + bonus) / 700)
		return DPS_multiplier

	def calc_increase(self)  -> float:
		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(float(self.stat_increase_entry.get()))
		increase = (stat_increase - stat) / (stat - 1) * 100
		return increase

	def set_progress(self):
		increase = self.calc_increase()
		self.progress.config(maximum=10)
		self.progress.config(value=increase)
		label3 = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20)
		label3.grid(row=self.stats_row, column=5)

	def get(self):
		return self.calc_DPS_increase()

class ElementAtk:
	def __init__(self, root, stat_increase: int, stats_row: int = 0, stat_name: str = 'Element ATK') -> None:
		self.stat_increase = stat_increase
		self.root = root
		self.stats_row = stats_row

		# row 1
		# base e.atk
		self.base_atk = tk.Label(self.root, text=f"base E-ATK:", anchor='w', width=15)
		self.base_atk.grid(row=self.stats_row, column=0)

		self.base_atk_entry = tk.Entry(self.root)
		self.base_atk_entry.insert(250, '250')
		self.base_atk_entry.grid(row=self.stats_row, column=1, padx= (0, 120))

		# increase
		self.label = tk.Label(self.root, text=f"+ {stat_name}:", anchor='w', width=20)
		self.label.grid(row=self.stats_row, column=2)

		self.stat_increase_entry = tk.Entry(self.root)
		self.stat_increase_entry.insert(stat_increase, str(stat_increase))
		self.stat_increase_entry.grid(row=self.stats_row, column=3, sticky='w')

		# progress_mod bar
		self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress.grid(row=self.stats_row, column=4, padx= (200,20))

		self.base_atk_entry.bind("<Return>", lambda e: self.set_progress())
		self.stat_increase_entry.bind("<Return>", lambda e: self.set_progress())

	def calc_DPS_increase(self, increase: float = 0) -> float:
		# get value
		base = float(self.base_atk_entry.get())
		# calculate increase
		DPS_multiplier = (1 + (base + increase) / 700)
		return DPS_multiplier

	def calc_increase(self)  -> float:

		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(float(self.stat_increase_entry.get()))
		increase = (stat_increase - stat) / (stat - 1) * 100
		return increase

	def set_progress(self):
		increase = self.calc_increase()
		self.progress.config(maximum=10)
		self.progress.config(value=increase)
		label3 = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20)
		label3.grid(row=self.stats_row, column=5)

	def get(self):
		return self.calc_DPS_increase()

class Crit:
	def __init__(self, root, stat_increase_mod: int, stat_increase_DMG: int, stats_row: int = 0) -> None:
		self.root = root
		self.stats_row = stats_row

		# row 1
		# crit mod
		self.crit_mod = tk.Label(self.root, text=f"CRIT mod:", anchor='w', width=15)
		self.crit_mod.grid(row=self.stats_row, column=0)

		self.crit_mod_entry = tk.Entry(self.root)
		self.crit_mod_entry.insert(100, '100')
		self.crit_mod_entry.grid(row=self.stats_row, column=1, padx= (0, 120))

		# increase crit mod
		self.label_mod = tk.Label(self.root, text=f"+ CRIT mod:", anchor='w', width=20)
		self.label_mod.grid(row=self.stats_row, column=2)

		self.stat_increase_mod_entry = tk.Entry(self.root)
		self.stat_increase_mod_entry.insert(stat_increase_mod, str(stat_increase_mod))
		self.stat_increase_mod_entry.grid(row=self.stats_row, column=3, sticky='w')

		#progress_mod bar
		self.progress_mod = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress_mod.grid(row=self.stats_row, column=4, padx= (200, 20))

		# row 2
		# bonus CRIT rate
		self.bonus_crit_rate = tk.Label(self.root, text='bonus CRIT rate:', anchor='w', width=15)
		self.bonus_crit_rate.grid(row=self.stats_row + 1, column = 0, pady=(0, 10))

		self.bonus_crit_rate_entry = tk.Entry(self.root)
		self.bonus_crit_rate_entry.insert(0, "0")
		self.bonus_crit_rate_entry.grid(row=self.stats_row + 1, column=1, padx=(0, 120), pady=(0, 10))

		# CRIT resist
		self.bonus_crit_resist = tk.Label(self.root, text='CRIT resist %:', anchor='w', width=20)
		self.bonus_crit_resist.grid(row=self.stats_row + 1, column=2, pady=(0, 10))

		self.bonus_crit_resist_entry = tk.Entry(self.root)
		self.bonus_crit_resist_entry.insert(0, "0")
		self.bonus_crit_resist_entry.grid(row=self.stats_row + 1, column=3, pady=(0, 10))


		#row 3
		# CRIT DMG
		self.crit_dmg = tk.Label(self.root, text='CRIT DMG:', anchor='w', width=15)
		self.crit_dmg.grid(row=self.stats_row + 2, column=0)

		self.crit_dmg_entry = tk.Entry(self.root)
		self.crit_dmg_entry.insert(50, "50")
		self.crit_dmg_entry.grid(row=self.stats_row + 2, column=1, sticky='w')

		# increase crit DMG
		self.label_DMG = tk.Label(self.root, text=f"+ CRIT DMG:", anchor='w', width=20)
		self.label_DMG.grid(row=self.stats_row + 2, column=2)

		self.stat_increase_DMG_entry = tk.Entry(self.root)
		self.stat_increase_DMG_entry.insert(stat_increase_DMG, str(stat_increase_DMG))
		self.stat_increase_DMG_entry.grid(row=self.stats_row + 2, column=3, sticky='w')

		#progess bar
		self.progress_DMG = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress_DMG.grid(row=self.stats_row + 2, column=4, padx=(200, 20))

		#row 4
		# bonus CRIT DMG
		self.b_crit_dmg = tk.Label(self.root, text='bonus CRIT DMG:', anchor='w', width=15)
		self.b_crit_dmg.grid(row=self.stats_row + 3, column=0)

		self.b_crit_dmg_entry = tk.Entry(self.root)
		self.b_crit_dmg_entry.insert(0, "0")
		self.b_crit_dmg_entry.grid(row=self.stats_row + 3, column=1, sticky='w')

		# triggers
		self.crit_mod_entry.bind("<Return>", lambda e: self.set_progress())
		self.bonus_crit_rate_entry.bind("<Return>", lambda e : self.set_progress())
		self.crit_dmg_entry.bind("<Return>", lambda e : self.set_progress())
		self.stat_increase_mod_entry.bind("<Return>", lambda e : self.set_progress_mod())
		self.stat_increase_DMG_entry.bind("<Return>", lambda e : self.set_progress_DMG())
		self.b_crit_dmg_entry.bind("<Return>", lambda e : self.set_progress())
		self.bonus_crit_resist_entry.bind("<Return>", lambda e : self.set_progress())

	def calc_DPS_increase(self, increase_mod: float = 0, increase_DMG: float = 0) -> float:
		# get value
		crit_mod = float(self.crit_mod_entry.get())
		crit_dmg = float(self.crit_dmg_entry.get())
		crit_mod += increase_mod
		crit_dmg += increase_DMG

		# calculate crit rate
		crit_rate = self.calc_crit_rate(crit_mod)

		DPS_multiplier = crit_dmg * crit_rate
		return DPS_multiplier

	def calc_increase_mod(self)  -> float:
		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(increase_mod= float(self.stat_increase_mod_entry.get()))
		increase = (stat_increase - stat) / (stat - 1) * 100 # todo: this equation doesn't work'
		return increase

	def calc_increase_DMG(self)  -> float:
		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(increase_DMG= float(self.stat_increase_DMG_entry.get()))
		increase = (stat_increase - stat) / (stat - 1) * 100
		return increase

	def set_progress_mod(self):
		increase = self.calc_increase_mod()
		crit_rate = self.calc_crit_rate(float(self.crit_mod_entry.get()))
		self.progress_mod.config(maximum=10)
		self.progress_mod.config(value=increase)

		label3 = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20)
		label3.grid(row=self.stats_row, column=5)

		label5 = tk.Label(self.root, text=f"{crit_rate * 100:.2f}% CRIT rate", anchor='w', width=20)
		label5.grid(row=self.stats_row + 1, column=4, padx=(200, 20))

	def set_progress_DMG(self):
		increase = self.calc_increase_DMG()
		self.progress_DMG.config(maximum=10)
		self.progress_DMG.config(value=increase)

		label4 = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20)
		label4.grid(row=self.stats_row + 2, column=5)

	def set_progress(self):
		self.set_progress_mod()
		self.set_progress_DMG()

	def get(self):
		return self.calc_DPS_increase()

	def calc_crit_rate(self, crit_mod: float) -> float:
		b_crit_rate = float(self.bonus_crit_rate_entry.get()) / 100

		# calculate increase
		if crit_mod <= 200 :
			crit_rate = crit_mod / 400
		if 200 < crit_mod <= 500 :
			crit_rate = crit_mod * 17 / 6000 - crit_mod ** 2 / 600000
		if 500 < crit_mod :
			crit_rate = crit_mod / 500
		crit_rate = crit_rate - float(self.bonus_crit_resist_entry.get()) / 100
		crit_rate += b_crit_rate
		crit_rate = crit_rate if crit_rate <= 1 else 1
		return crit_rate

class SkillBasicEle:
	def __init__(self, root, stat_increase: int, stat_name: str, stats_row: int = 0) -> None:
		self.stat_increase = stat_increase
		self.root = root
		self.stats_row = stats_row

		# row 1
		# base stat
		self.stat_label = tk.Label(self.root, text=f"{stat_name}:", anchor='w', width=15)
		self.stat_label.grid(row=self.stats_row, column=0)

		self.stat_entry = tk.Entry(self.root)
		self.stat_entry.insert(0, '0')
		self.stat_entry.grid(row=self.stats_row, column=1, padx= (0, 120))

		# increase
		self.label = tk.Label(self.root, text=f"+ {stat_name}:", anchor='w', width=20)
		self.label.grid(row=self.stats_row, column=2)

		self.stat_increase_entry = tk.Entry(self.root)
		self.stat_increase_entry.insert(stat_increase, str(stat_increase))
		self.stat_increase_entry.grid(row=self.stats_row, column=3, sticky='w')

		# progress_mod bar
		self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress.grid(row=self.stats_row, column=4, padx= (200,20))

		self.stat_entry.bind("<Return>", lambda e: self.set_progress())
		self.stat_increase_entry.bind("<Return>", lambda e: self.set_progress())

	def calc_DPS_increase(self, increase: float = 0) -> float:
		# get value
		base = float(self.stat_entry.get()) / 100
		# calculate increase
		DPS_multiplier = 1 + (base + increase / 100)
		return DPS_multiplier

	def calc_increase(self)  -> float:

		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(float(self.stat_increase_entry.get()))
		increase = (stat_increase - stat) / (stat - 1) * 100
		return increase

	def set_progress(self):
		increase = self.calc_increase()
		self.progress.config(maximum=10)
		self.progress.config(value=increase)
		label3 = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20)
		label3.grid(row=self.stats_row, column=5)

	def get(self):
		return self.calc_DPS_increase()

class DefIgn:
	def __init__(self, root, stat_increase: int, stats_row: int = 0) -> None:
		self.stat_increase = stat_increase
		self.root = root
		self.stats_row = stats_row

		# row 1
		# Def Ignore
		self.label = tk.Label(self.root, text=f"DEF Ignore:", anchor='w', width=15)
		self.label.grid(row=self.stats_row, column=0)

		self.def_ignore_entry = tk.Entry(self.root)
		self.def_ignore_entry.insert(5000, '5000')
		self.def_ignore_entry.grid(row=self.stats_row, column=1, padx= (0, 120))

		# increase
		self.label1 = tk.Label(self.root, text=f"+ DEF Ignore:", anchor='w', width=20)
		self.label1.grid(row=self.stats_row, column=2)

		self.stat_increase_entry = tk.Entry(self.root)
		self.stat_increase_entry.insert(stat_increase, str(stat_increase))
		self.stat_increase_entry.grid(row=self.stats_row, column=3, sticky='w')

		#progress_mod
		self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress.grid(row=self.stats_row , column=4, padx= (200,20))

		# row 2
		# enemy Def
		self.label2 = tk.Label(self.root, text= 'enemy DEF:', anchor='w', width=15)
		self.label2.grid(row=self.stats_row + 1, column = 0)

		self.def_entry = tk.Entry(self.root)
		self.def_entry.insert(6800, "6800")
		self.def_entry.grid(row=self.stats_row + 1, column=1, padx=(0, 120))

		# Def shred
		self.label3 = tk.Label(self.root, text='DEF shred:', anchor='w', width=20)
		self.label3.grid(row=self.stats_row + 1, column=2)

		self.def_shred_entry = tk.Entry(self.root)
		self.def_shred_entry.insert(0, "0")
		self.def_shred_entry.grid(row=self.stats_row + 1, column=3, sticky='w')

		# row 3
		# Def shred %
		self.label4 = tk.Label(self.root, text='DEF shred %:', anchor='w', width=15)
		self.label4.grid(row=self.stats_row + 2, column=0)

		self.def_shred_per_entry = tk.Entry(self.root)
		self.def_shred_per_entry.insert(0, "0")
		self.def_shred_per_entry.grid(row=self.stats_row + 2, column=1, padx=(0, 120))


		# triggers
		self.def_shred_entry.bind("<Return>", lambda e: self.set_progress())
		self.def_entry.bind("<Return>", lambda e : self.set_progress())
		self.def_shred_per_entry.bind("<Return>", lambda e : self.set_progress())
		self.stat_increase_entry.bind("<Return>", lambda e : self.set_progress())
		self.def_ignore_entry.bind("<Return>", lambda e : self.set_progress())

	def calc_DPS_increase(self, increase: float = 0) -> float:
		# get value
		di = float(self.def_ignore_entry.get()) + increase
		defense = self.calc_def()
		delta = defense - di

		if delta <= 0:
			DPS_multiplier = 1
		else:
			DPS_multiplier = 1505 / (1505 + delta)

		return DPS_multiplier

	def calc_increase(self)  -> float:
		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(float(self.stat_increase_entry.get()))
		increase = (stat_increase - stat) * 100
		return increase

	def set_progress(self):
		increase = self.calc_increase()
		damage_lost = (1 - self.calc_DPS_increase()) * 100
		self.progress.config(maximum=10)
		self.progress.config(value=increase)
		label = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20)
		label.grid(row=self.stats_row, column=5)

		label2 = tk.Label(self.root, text=f"losing {damage_lost:.2f}% DPS to DI", anchor='w', width=20)
		label2.grid(row=self.stats_row + 1, column=4, padx=(200, 20))

	def calc_def(self) -> float:
		# get value
		base = float(self.def_entry.get())
		per_shred = float(self.def_shred_per_entry.get()) / 100
		flat_shred = float(self.def_shred_entry.get())

		defense = base * (1 - per_shred) - flat_shred
		return defense

	def get(self):
		return self.calc_DPS_increase()

class Ep:
	def __init__(self, root, stat_increase: int, stats_row: int = 0) -> None:
		self.stat_increase = stat_increase
		self.root = root
		self.stats_row = stats_row

		# row 1
		# Def Ignore
		self.label = tk.Label(self.root, text=f"EP:", anchor='w', width=15)
		self.label.grid(row=self.stats_row, column=0)

		self.ep_entry = tk.Entry(self.root)
		self.ep_entry.insert(1500, '1000')
		self.ep_entry.grid(row=self.stats_row, column=1, padx= (0, 120))

		# increase
		self.label1 = tk.Label(self.root, text=f"+ EP:", anchor='w', width=20)
		self.label1.grid(row=self.stats_row, column=2)

		self.stat_increase_entry = tk.Entry(self.root)
		self.stat_increase_entry.insert(stat_increase, str(stat_increase))
		self.stat_increase_entry.grid(row=self.stats_row, column=3, sticky='w')

		#progress_mod
		self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress.grid(row=self.stats_row , column=4, padx= (200,20))

		# row 2
		# enemy Def
		self.label2 = tk.Label(self.root, text= 'enemy E DEF:', anchor='w', width=15)
		self.label2.grid(row=self.stats_row + 1, column = 0)

		self.e_def_entry = tk.Entry(self.root)
		self.e_def_entry.insert(2600, "2600")
		self.e_def_entry.grid(row=self.stats_row + 1, column=1, padx=(0, 120))

		# Def shred
		self.label3 = tk.Label(self.root, text='EP shred:', anchor='w', width=20)
		self.label3.grid(row=self.stats_row + 1, column=2)

		self.e_def_shred_entry = tk.Entry(self.root)
		self.e_def_shred_entry.insert(0, "0")
		self.e_def_shred_entry.grid(row=self.stats_row + 1, column=3, sticky='w')


		# triggers
		self.e_def_shred_entry.bind("<Return>", lambda e: self.set_progress())
		self.e_def_entry.bind("<Return>", lambda e : self.set_progress())
		self.stat_increase_entry.bind("<Return>", lambda e : self.set_progress())
		self.ep_entry.bind("<Return>", lambda e : self.set_progress())

	def calc_DPS_increase(self, increase: float = 0) -> float:
		# get value
		ep = float(self.ep_entry.get()) + increase
		e_defense = self.calc_def()

		if ep > e_defense:
			DPS_multiplier = 1 + ((ep - e_defense) / ( ep- e_defense + 3992))
		else:
			DPS_multiplier = 1505 / (1505 + e_defense - ep)

		return DPS_multiplier

	def calc_increase(self)  -> float:
		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(float(self.stat_increase_entry.get()))
		increase = (stat_increase - stat) * 100
		return increase

	def set_progress(self):
		increase = self.calc_increase()
		damage_lost = (1 - self.calc_DPS_increase()) * 100
		self.progress.config(maximum=10)
		self.progress.config(value=increase)
		label = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20)
		label.grid(row=self.stats_row, column=5)

		if damage_lost > 0:
			text = f"losing {damage_lost:.2f}% DPS to EP"
		else:
			text = "no losing DPS to EP"
		label2 = tk.Label(self.root, text=text, anchor='w', width=20)
		label2.grid(row=self.stats_row + 1, column=4, padx=(200, 20))

	def calc_def(self) -> float:
		# get value
		base = float(self.e_def_entry.get())
		flat_shred = float(self.e_def_shred_entry.get())

		e_defense = base - flat_shred
		return e_defense

	def get(self):
		return self.calc_DPS_increase()



if __name__ == '__main__':
	main()
