from phaseportrait import PhasePortrait2D
# from .Trajectories2D import Trajectory2D
# from .Trajectories3D import Trajectory3D
# from .Map1D import Map1D
# from .Cobweb import Cobweb

import sys
import re
import matplotlib.pyplot as plt
import json
import time

class PhasePortrait2DManager(object):
    @staticmethod
    def plot_from_json(json_str: str) -> str:
        """Returns a string containing SVG figure path for json given."""
        info = json.loads(json_str)
        
        representation = PhasePortrait2D(lambda x,y:(x,y), [-1,1])
        
        # Function
        try:
            match = re.search(r"def\s+(\w+)\(", info['dF'])
            function_name = match.group(1)
            match = re.search(r"(\s+)def", info['dF'])
            if match is not None:
                info['dF'] = info['dF'].replace(match.group(0), "def")
            del match
            
            exec(info['dF'], globals())
            representation.dF = globals()[function_name]
        except  Exception as e:
            return 0
        
        # Range
        representation.Range = [[info['Range']['x_min'],info['Range']['x_max']],
                                [info['Range']['y_min'],info['Range']['y_max']]]
        
        # Parameters
        kargs = ['MeshDim', 'dF_args', 'Density', 'Polar', 'Title', 'xlabel', 'ylabel', 'color']
        for k,v in info.items():
            if k in kargs:
                setattr(representation, k, v)

        # Nullcline
        if nc:=info['nullcline']:
            representation.add_nullclines(**nc)
        
        
        # Plot and save
        fig, ax = representation.plot()
        
        path = ""
        fig_name = time.strftime('%a%d%b%Y%H%M%SGMT',time.localtime())
        fig.savefig(path + fig_name +'.svg')
        return path
    
    
    @staticmethod
    def json_to_python_code(json_str: str) -> str:
        """Returns a string containing equivalent Python code for the json given."""
        
        info = json.loads(json_str)
        
        match = re.search(r"def\s+(\w+)\(", info['dF'])
        function_name = match.group(1)

        header = f"""from phaseportrait import *\nimport matplotlib.pyplot as plt"""

        function = f"""\n{info['dF']}"""

        portrait = f"""\nphase_diagram = PhasePortrait2D({function_name}, [[{info['Range']['x_min']},{info['Range']['x_max']}],[{info['Range']['y_min']},{info['Range']['y_max']}]],"""
        
        portrait_kargs = ""
        kargs = ['MeshDim', 'dF_args', 'Density', 'Polar', 'Title', 'xlabel', 'ylabel', 'color']
        first = True
        for k in info.keys():
            if k in kargs:
                if info[k]:
                    if isinstance(info[k], str):
                        portrait_kargs += f"\t{k} = '{info[k]}',\n"
                    else:
                        portrait_kargs += f"\t{k} = {info[k]},\n"
                    first = False
        if first:
            portrait += ')\n'
        else:
            portrait_kargs += ')\n'
        
        nullcline = ''
        if nc := info.get('nullcline'):
            nullcline = f"\nphase_diagram.add_nullclines(precision={nc['precision']}, offset={nc['offset']})"
        
        finisher = '\nphase_diagram.plot()\nplt.show()'

        return "\n".join([header, function, portrait, portrait_kargs, nullcline, finisher])

    @staticmethod
    def echo(self, text) -> str:
        """echo any text"""
        return text


# if __name__ == '__main__':
#     api = PhasePortrait2DManager()
#     code = ''
    
#     with open("phaseportrait/phaseportrait2d.json", 'r') as file:
#         code = "\n".join(file.readlines())
#         code = api.json_to_python_code(code)

#     with open('prueba.py', 'w') as o_file:
#         o_file.write(code)


if __name__ == '__main__':
    with open("phaseportrait/phaseportrait2d.json", 'r') as file:
        code = "\n".join(file.readlines())
        PhasePortrait2DManager.plot_from_json(code)