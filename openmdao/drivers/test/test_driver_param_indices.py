""" Testing optimizer ScipyOptimize."""

import unittest

import numpy as np

from openmdao.core import Problem, Group
from openmdao.components import IndepVarComp, ExecComp
from openmdao.drivers import ScipyOptimizer
from openmdao.solvers import LinearGaussSeidel
from openmdao.test.sellar import SellarStateConnection
from openmdao.test.util import assert_rel_error

SKIP = False
try:
    from openmdao.drivers.pyoptsparse_driver import pyOptSparseDriver
except ImportError:
    # Just so python can parse this file.
    from openmdao.core.driver import Driver
    pyOptSparseDriver = Driver
    SKIP = True


class TestParamIndices(unittest.TestCase):

    def setUp(self):
        if SKIP is True:
            raise unittest.SkipTest("Could not import pyOptSparseDriver. "
                                    "Is pyoptsparse installed?")

    def test_Sellar_state_SLSQP(self):
        """ Baseline Sellar test case without specifying indices.
        """

        prob = Problem()
        prob.root = SellarStateConnection()

        prob.driver = ScipyOptimizer()
        prob.driver.options['optimizer'] = 'SLSQP'
        prob.driver.options['tol'] = 1.0e-8

        prob.driver.add_desvar('z', low=np.array([-10.0, 0.0]),
                                    high=np.array([10.0, 10.0]))
        prob.driver.add_desvar('x', low=0.0, high=10.0)

        prob.driver.add_objective('obj')
        prob.driver.add_constraint('con1', upper=0.0)
        prob.driver.add_constraint('con2', upper=0.0)
        prob.driver.options['disp'] = False

        prob.setup(check=False)
        prob.run()

        assert_rel_error(self, prob['z'][0], 1.9776, 1e-3)
        assert_rel_error(self, prob['z'][1], 0.0, 1e-3)
        assert_rel_error(self, prob['x'], 0.0, 1e-3)

    def test_driver_param_indices_slsqp(self):
        """ Test driver param indices with ScipyOptimizer SLSQP and force_fd=False
        """

        prob = Problem()
        prob.root = SellarStateConnection()

        prob.driver = ScipyOptimizer()
        prob.driver.options['optimizer'] = 'SLSQP'
        prob.driver.options['tol'] = 1.0e-8
        prob.root.fd_options['force_fd'] = False

        prob.driver.add_desvar('z', low=np.array([-10.0]),
                                    high=np.array([10.0]), indices=[0])
        prob.driver.add_desvar('x', low=0.0, high=10.0)

        prob.driver.add_objective('obj')
        prob.driver.add_constraint('con1', upper=0.0)
        prob.driver.add_constraint('con2', upper=0.0)
        #prob.driver.options['disp'] = False

        prob.setup(check=False)

        prob['z'][1] = 0.0

        prob.run()

        assert_rel_error(self, prob['z'][0], 1.9776, 1e-3)
        assert_rel_error(self, prob['z'][1], 0.0, 1e-3)
        assert_rel_error(self, prob['x'], 0.0, 1e-3)

    def test_driver_param_indices_slsqp_force_fd(self):
        """ Test driver param indices with ScipyOptimizer SLSQP and force_fd=True
        """

        prob = Problem()
        prob.root = SellarStateConnection()
        prob.root.fd_options['force_fd'] = True

        prob.driver = ScipyOptimizer()
        prob.driver.options['optimizer'] = 'SLSQP'
        prob.driver.options['tol'] = 1.0e-8

        prob.driver.add_desvar('z', low=np.array([-10.0]),
                                    high=np.array([10.0]), indices=[0])
        prob.driver.add_desvar('x', low=0.0, high=10.0)

        prob.driver.add_objective('obj')
        prob.driver.add_constraint('con1', upper=0.0)
        prob.driver.add_constraint('con2', upper=0.0)
        #prob.driver.options['disp'] = False

        prob.setup(check=False)

        prob['z'][1] = 0.0

        prob.run()

        assert_rel_error(self, prob['z'][0], 1.9776, 1e-3)
        assert_rel_error(self, prob['z'][1], 0.0, 1e-3)
        assert_rel_error(self, prob['x'], 0.0, 1e-3)

    def test_driver_param_indices_snopt(self):
        """ Test driver param indices with pyOptSparse and force_fd=False
        """

        prob = Problem()
        prob.root = SellarStateConnection()
        prob.root.fd_options['force_fd'] = False

        prob.driver = pyOptSparseDriver()

        prob.driver.add_desvar('z', low=np.array([-10.0]),
                                    high=np.array([10.0]), indices=[0])
        prob.driver.add_desvar('x', low=0.0, high=10.0)

        prob.driver.add_objective('obj')
        prob.driver.add_constraint('con1', upper=0.0)
        prob.driver.add_constraint('con2', upper=0.0)

        prob.setup(check=False)

        prob['z'][1] = 0.0

        prob.run()

        assert_rel_error(self, prob['z'][0], 1.9776, 1e-3)
        assert_rel_error(self, prob['z'][1], 0.0, 1e-3)
        assert_rel_error(self, prob['x'], 0.0, 1e-3)

    def test_driver_param_indices_snopt_force_fd(self):
        """ Test driver param indices with pyOptSparse and force_fd=True
        """

        prob = Problem()
        prob.root = SellarStateConnection()
        prob.root.fd_options['force_fd'] = True

        prob.driver = pyOptSparseDriver()

        prob.driver.add_desvar('z', low=np.array([-10.0]),
                                    high=np.array([10.0]), indices=[0])
        prob.driver.add_desvar('x', low=0.0, high=10.0)

        prob.driver.add_objective('obj')
        prob.driver.add_constraint('con1', upper=0.0)
        prob.driver.add_constraint('con2', upper=0.0)
        #prob.driver.options['disp'] = False

        prob.setup(check=False)

        prob['z'][1] = 0.0

        prob.run()

        assert_rel_error(self, prob['z'][0], 1.9776, 1e-3)
        assert_rel_error(self, prob['z'][1], 0.0, 1e-3)
        assert_rel_error(self, prob['x'], 0.0, 1e-3)

    def test_driver_param_indices_snopt_force_fd_shift(self):
        """ Test driver param indices with pyOptSparse and force_fd=True
        """

        prob = Problem()
        prob.root = SellarStateConnection()
        prob.root.fd_options['force_fd'] = True

        prob.driver.add_desvar('z', low=np.array([-10.0, -10.0]),
                                    high=np.array([10.0, 10.0]), indices=[1])
        prob.driver.add_desvar('x', low=0.0, high=10.0)

        prob.driver.add_objective('obj')
        prob.driver.add_constraint('con1', upper=0.0)
        prob.driver.add_constraint('con2', upper=0.0)
        #prob.driver.options['disp'] = False

        prob.setup(check=False)

        prob['z'][1] = 0.0

        prob.run()

        J = prob.calc_gradient(['x', 'z'], ['obj'], mode='fd',
                               return_format='array')
        assert_rel_error(self, J[0][1], 1.78402, 1e-3)

    def test_poi_index_w_irrelevant_var(self):
        prob = Problem()
        prob.driver = pyOptSparseDriver()
        prob.root = root = Group()
        prob.root.ln_solver = LinearGaussSeidel()
        prob.root.ln_solver.options['single_voi_relevance_reduction'] = True
        prob.root.ln_solver.options['mode'] = 'rev'

        root.add('p1', IndepVarComp('x', np.array([1.0, 3.0, 4.0])))
        root.add('p2', IndepVarComp('x', np.array([5.0, 2.0, -1.0])))
        root.add('C1', ExecComp('y = 2.0*x', x=np.zeros(3), y=np.zeros(3)))
        root.add('C2', ExecComp('y = 3.0*x', x=np.zeros(3), y=np.zeros(3)))
        root.add('con1', ExecComp('c = 7.0 - y', y=np.zeros(3), c=np.zeros(3)))
        root.add('con2', ExecComp('c = 2.0 - y', y=np.zeros(3), c=np.zeros(3)))
        root.add('obj', ExecComp('o = y1+y2'))

        prob.driver.add_desvar('p1.x', indices=[1])
        prob.driver.add_desvar('p2.x', indices=[2])
        prob.driver.add_constraint('con1.c', upper=0.0, indices=[1])
        prob.driver.add_constraint('con2.c', upper=0.0, indices=[2])
        prob.driver.add_objective('obj.o')

        root.connect('p1.x', 'C1.x')
        root.connect('p2.x', 'C2.x')
        root.connect('C1.y', 'con1.y')
        root.connect('C2.y', 'con2.y')
        root.connect('C1.y', 'obj.y1', src_indices=[1])
        root.connect('C2.y', 'obj.y2', src_indices=[2])

        prob.setup(check=False)
        prob.run()

        # I was trying in this test to duplicate an error in pointer, but wasn't able to.
        # I was able to find a different error that occurred when using return_format='array'
        # that was also fixed by the same PR that fixed pointer.
        J = prob.calc_gradient(['p1.x', 'p2.x'], ['con1.c', 'con2.c'], mode='rev',
                               return_format='array')

        assert_rel_error(self, J[0][0], -2.0, 1e-3)
        assert_rel_error(self, J[0][1], .0, 1e-3)
        assert_rel_error(self, J[1][0], .0, 1e-3)
        assert_rel_error(self, J[1][1], -3.0, 1e-3)

        J = prob.calc_gradient(['p1.x', 'p2.x'], ['con1.c', 'con2.c'], mode='rev',
                               return_format='dict')

        assert_rel_error(self, J['con1.c']['p1.x'], -2.0, 1e-3)
        assert_rel_error(self, J['con1.c']['p2.x'], .0, 1e-3)
        assert_rel_error(self, J['con2.c']['p1.x'], .0, 1e-3)
        assert_rel_error(self, J['con2.c']['p2.x'], -3.0, 1e-3)


if __name__ == "__main__":
    unittest.main()
